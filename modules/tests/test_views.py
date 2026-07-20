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


# --------------------------------------------------------------------------
# Dashboard — real data from the database
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_shows_real_points_after_completing_lessons(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    complete(client_student, modules[0], 2, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    # 2 lessons × 10 = 20 points. The redesigned dashboard frames points as
    # level XP; at 20 points you're 20 short of level 2.
    assert "20 points" in html


@pytest.mark.django_db
def test_dashboard_reflects_earned_badges(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "First step" in html          # the badge name
    assert "cy-badge--earned" in html


@pytest.mark.django_db
def test_dashboard_continue_points_at_the_next_lesson(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert reverse("learn:module", args=[1]) in html
    assert "Pick up where you left off" in html


# --------------------------------------------------------------------------
# Rendering hygiene — no template leaks, no emoji, on the new pages
# --------------------------------------------------------------------------

import re

LEAKS = ["{#", "#}", "{%", "%}", "{{", "}}"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


@pytest.mark.django_db
def test_learn_pages_render_clean_and_without_emoji(client_student, modules):
    urls = [
        reverse("learn:browser"),
        reverse("learn:module", args=[1]),
        reverse("learn:lesson", args=[1, 1]),
        reverse("learn:simulation", args=[1]),
        reverse("learn:progress"),
        reverse("learn:badges"),
        reverse("learn:certificate"),
        reverse("dashboard"),
    ]
    for url in urls:
        html = client_student.get(url).content.decode()
        for token in LEAKS:
            assert token not in html, f"{url} leaked {token!r}"
        assert not EMOJI.findall(html), f"{url} contains emoji"


# --------------------------------------------------------------------------
# The app shell — sidebar, active state, new pages
# --------------------------------------------------------------------------

STUDENT_PATHS = [
    ("learn:browser", []),
    ("dashboard", []),
    ("learn:progress", []),
    ("learn:badges", []),
    ("learn:certificate", []),
    ("learn:module", [1]),
    ("learn:lesson", [1, 1]),
    ("learn:simulation", [1]),
]


@pytest.mark.django_db
def test_every_student_page_lives_in_the_app_shell(client_student, modules):
    for name, args in STUDENT_PATHS:
        html = client_student.get(reverse(name, args=args)).content.decode()
        assert 'class="cy-side__nav"' in html, name
        # the mobile drawer toggle, wired to the sidebar
        assert 'aria-controls="cy-side"' in html, name


@pytest.mark.django_db
def test_sidebar_links_to_every_section(client_student, modules):
    html = client_student.get(reverse("dashboard")).content.decode()
    for name in ["dashboard", "learn:browser", "learn:progress", "learn:badges", "learn:certificate"]:
        assert reverse(name) in html


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name,active_key",
    [("dashboard", "Dashboard"), ("learn:progress", "My progress"), ("learn:badges", "Badges")],
)
def test_the_right_sidebar_item_is_active(client_student, modules, name, active_key):
    html = client_student.get(reverse(name)).content.decode()
    # the active item and its label appear together
    marker = 'cy-side__item is-active'
    assert marker in html
    idx = html.index(marker)
    assert active_key in html[idx : idx + 200]


@pytest.mark.django_db
def test_new_pages_show_real_data(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    progress = client_student.get(reverse("learn:progress")).content.decode()
    assert modules[0].title in progress

    badges = client_student.get(reverse("learn:badges")).content.decode()
    assert "First step" in badges and "cy-badge-card" in badges

    cert = client_student.get(reverse("learn:certificate")).content.decode()
    assert "certificate" in cert.lower()


@pytest.mark.django_db
def test_new_pages_require_login(client, modules):
    for name in ["learn:progress", "learn:badges", "learn:certificate"]:
        response = client.get(reverse(name))
        assert response.status_code == 302
        assert "/login/" in response.url


# --------------------------------------------------------------------------
# Dashboard — momentum redesign
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_brand_new_student_gets_the_welcome_state_not_bare_zeros(client_student, modules):
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-welcome" in html
    assert "Welcome to" in html
    # exactly one primary action, even here
    assert html.count("cy-btn--primary") == 1


@pytest.mark.django_db
def test_a_returning_student_sees_the_continue_hero_and_rank(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-hero-continue" in html
    assert "Cyber Aware" in html                 # the rank title
    assert html.count("cy-btn--primary") == 1    # the single Continue


@pytest.mark.django_db
def test_the_roadmap_marks_the_current_module(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-road" in html
    assert "is-current" in html                  # the pulsing "you are here" stop
    assert "Certified" in html                   # the journey's end


@pytest.mark.django_db
def test_the_streak_nudges_when_a_day_is_at_risk(client_student, student, modules):
    import datetime

    from django.utils import timezone

    # Active yesterday, not yet today → at risk.
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    profile = student.profile
    profile.streak_count = 4
    profile.last_active = timezone.make_aware(
        datetime.datetime.combine(
            timezone.localdate() - datetime.timedelta(days=1), datetime.time(12, 0)
        )
    )
    profile.save(update_fields=["streak_count", "last_active"])

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-streak-card--at_risk" in html
    assert "keep your 4-day streak" in html
