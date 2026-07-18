"""The student-facing views: browser, overview, lesson, completion, simulation.

The load-bearing assertions are the lock (a real 403 from the view, not a hidden
link) and that completion awards real points once.
"""

import json

import pytest
from django.urls import reverse

from modules.models import ProgressRecord, SimulationResult


@pytest.fixture
def client_student(client, student):
    client.force_login(student)
    return client


def complete(client, module, lesson_number, **extra):
    return client.post(
        reverse("learn:complete_lesson", args=[module.order_index, lesson_number]),
        **extra,
    )


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_the_whole_learn_area_requires_login(client, modules):
    for name, args in [
        ("learn:browser", []),
        ("learn:module", [1]),
        ("learn:lesson", [1, 1]),
        ("learn:simulation", [1]),
    ]:
        response = client.get(reverse(name, args=args))
        assert response.status_code == 302
        assert "/login/" in response.url, name


# --------------------------------------------------------------------------
# Browser + overview
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_browser_lists_the_published_modules(client_student, modules):
    html = client_student.get(reverse("learn:browser")).content.decode()
    for m in modules:
        assert m.title in html


@pytest.mark.django_db
def test_overview_of_the_first_module_is_reachable(client_student, modules):
    assert client_student.get(reverse("learn:module", args=[1])).status_code == 200


# --------------------------------------------------------------------------
# The lock — enforced in the view, not just hidden
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_locked_module_overview_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:module", args=[2])).status_code == 403


@pytest.mark.django_db
def test_a_locked_module_lesson_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:lesson", args=[2, 1])).status_code == 403


@pytest.mark.django_db
def test_a_locked_module_simulation_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:simulation", args=[2])).status_code == 403


@pytest.mark.django_db
def test_finishing_a_module_unlocks_the_next_overview(client_student, modules):
    for n in range(1, 5):
        complete(client_student, modules[0], n)
    assert client_student.get(reverse("learn:module", args=[2])).status_code == 200


# --------------------------------------------------------------------------
# Lesson + completion
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_lesson_renders_its_body(client_student, modules):
    response = client_student.get(reverse("learn:lesson", args=[1, 1]))
    assert response.status_code == 200
    assert b"Placeholder" in response.content


@pytest.mark.django_db
def test_marking_complete_records_progress_and_awards_ten(client_student, student, modules):
    response = complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    data = json.loads(response.content)

    assert data["points_gained"] == 10
    assert data["points"] == 10
    assert ProgressRecord.objects.filter(user=student, lesson__module=modules[0]).count() == 1


@pytest.mark.django_db
def test_marking_complete_twice_awards_once(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    second = complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    data = json.loads(second.content)

    assert data["points_gained"] == 0
    assert data["points"] == 10
    assert ProgressRecord.objects.filter(user=student).count() == 1


@pytest.mark.django_db
def test_completion_without_js_redirects_to_the_next_lesson(client_student, modules):
    response = complete(client_student, modules[0], 1)
    assert response.status_code == 302
    assert response.url == reverse("learn:lesson", args=[1, 2])


@pytest.mark.django_db
def test_completion_is_post_only(client_student, modules):
    url = reverse("learn:complete_lesson", args=[1, 1])
    assert client_student.get(url).status_code == 405


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_simulation_page_renders_with_the_scenario_data(client_student, modules):
    response = client_student.get(reverse("learn:simulation", args=[1]))
    assert response.status_code == 200
    assert b'id="cy-sim-data"' in response.content


@pytest.mark.django_db
def test_completing_a_simulation_stores_the_result(client_student, student, modules):
    response = client_student.post(
        reverse("learn:complete_simulation", args=[1]),
        data=json.dumps({"score": 1, "total": 1, "path": [{"id": "a", "correct": True}]}),
        content_type="application/json",
    )
    assert response.status_code == 200
    result = SimulationResult.objects.get(user=student, simulation=modules[0].simulation)
    assert result.score == 1
    assert result.total == 1


@pytest.mark.django_db
def test_a_tampered_simulation_score_is_clamped(client_student, student, modules):
    """A client posting score 99 out of 1 shouldn't be believed."""
    client_student.post(
        reverse("learn:complete_simulation", args=[1]),
        data=json.dumps({"score": 99, "total": 1, "path": []}),
        content_type="application/json",
    )
    result = SimulationResult.objects.get(user=student)
    assert result.score == 1  # clamped to total


@pytest.mark.django_db
def test_browser_query_count_is_bounded(client_student, make_module, django_assert_max_num_queries):
    for i in range(1, 7):
        make_module(i)
    # Whatever the fixed cost is, it must not grow with module count. Generous
    # ceiling: auth, session, profile, and the two progress queries.
    with django_assert_max_num_queries(12):
        client_student.get(reverse("learn:browser"))
