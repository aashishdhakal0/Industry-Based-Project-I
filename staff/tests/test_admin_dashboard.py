"""The Administrator dashboard: access control, the aggregates, sort/filter, CSV.

A small but complete world is built in the `world` fixture:

  - Two modules, each with two lessons and a quiz.
  - alice  — both modules done, quizzes best-of 100 and 80  -> Distinction, course complete.
  - bob    — module 1 done (quiz 70 = Pass), module 2 untouched -> Pass, 1/2.
  - carol  — nothing -> Not started, 0/2.
"""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult

PASSWORD = "correct-horse-battery"


def make_student(email, first, points=0, days_ago=None):
    user = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Test",
        role=User.Role.STUDENT, is_verified=True,
    )
    last = timezone.now() - timedelta(days=days_ago) if days_ago is not None else None
    UserProfile.objects.create(user=user, points=points, last_active=last,
                               organisation="Docklands Dental")
    return user


def complete_lessons(user, module):
    for lesson in module.lessons.all():
        ProgressRecord.objects.create(user=user, lesson=lesson)


def attempt(user, quiz, score, attempt_number=1):
    QuizResult.objects.create(
        user=user, quiz=quiz, score=score, passed=score >= quiz.pass_mark,
        attempt_number=attempt_number,
    )


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)

    modules = {}
    for i in (1, 2):
        m = Module.objects.create(
            title=f"Module {i}", order_index=i, is_published=True, created_by=admin
        )
        for n in (1, 2):
            Lesson.objects.create(module=m, lesson_number=n, title=f"L{n}")
        m.quiz_obj = Quiz.objects.create(module=m, is_active=True, pass_mark=70)
        modules[i] = m

    alice = make_student("alice@example.com", "Alice", points=300, days_ago=1)
    complete_lessons(alice, modules[1])
    complete_lessons(alice, modules[2])
    attempt(alice, modules[1].quiz_obj, 60, attempt_number=1)   # a fail first
    attempt(alice, modules[1].quiz_obj, 100, attempt_number=2)  # best counts
    attempt(alice, modules[2].quiz_obj, 80)

    bob = make_student("bob@example.com", "Bob", points=120, days_ago=10)
    complete_lessons(bob, modules[1])
    attempt(bob, modules[1].quiz_obj, 70)

    carol = make_student("carol@example.com", "Carol", points=0)

    return {"modules": modules, "alice": alice, "bob": bob, "carol": carol,
            "admin": admin}


# --- Access control (a real 403, not a hidden link) ------------------------


@pytest.mark.parametrize("name", ["staff:overview", "staff:learners", "staff:learners_csv"])
def test_anonymous_is_sent_to_login(client, world, name):
    resp = client.get(reverse(name))
    assert resp.status_code == 302
    assert reverse("authentication:login") in resp.url


@pytest.mark.parametrize("name", ["staff:overview", "staff:learners", "staff:learners_csv"])
def test_student_is_forbidden(client, world, name):
    client.force_login(world["alice"])
    assert client.get(reverse(name)).status_code == 403


@pytest.mark.parametrize("name", ["staff:overview", "staff:learners"])
def test_administrator_gets_in(client, world, name):
    client.force_login(world["admin"])
    assert client.get(reverse(name)).status_code == 200


# --- Overview stats --------------------------------------------------------


def test_overview_stats_are_right(client, world):
    from staff import services

    stats = services.overview(services.collect_learners())
    assert stats["total_learners"] == 3
    assert stats["completed_course"] == 1            # alice
    assert stats["completion_rate"] == 33            # 1 of 3
    assert stats["average_score"] == 80              # mean of 90 (alice) and 70 (bob)
    assert stats["not_started"] == 1                 # carol

    dist = {d["tier"].slug: d["count"] for d in stats["distribution"]}
    assert dist == {"distinction": 1, "merit": 0, "pass": 1, "not-yet": 0}


def test_overview_page_renders_headline_numbers(client, world):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:overview")).content.decode()
    assert "Learners" in body
    assert "Completion" in body
    assert "Average score" in body
    assert "cy-app--console" in body        # the console theme is scoped on


def test_overview_organisation_rollup(world):
    """The per-organisation rollup (now surfaced on the Organisations page)."""
    from staff import services

    stats = services.overview(services.collect_learners())
    orgs = stats["organisations"]
    assert orgs                                            # non-empty
    assert sum(o["count"] for o in orgs) == stats["total_learners"]
    # All three learners share the one org in this fixture.
    assert orgs[0]["name"] == "Docklands Dental"
    assert orgs[0]["count"] == 3


# --- Learner rows: completion + best-of-attempts grading -------------------


def test_learner_rows_compute_completion_and_grade(client, world):
    from staff import services

    rows = {r.user.email: r for r in services.collect_learners()}

    alice = rows["alice@example.com"]
    assert alice.modules_completed == 2 and alice.modules_total == 2
    assert alice.completed_course is True
    assert alice.overall_score == 90               # best-of: (100 + 80) / 2
    assert alice.tier.slug == "distinction"

    bob = rows["bob@example.com"]
    assert bob.modules_completed == 1
    assert bob.completed_course is False
    assert bob.overall_score == 70
    assert bob.tier.slug == "pass"

    carol = rows["carol@example.com"]
    assert carol.modules_completed == 0
    assert carol.overall_score is None
    assert carol.tier.slug == "not-started"


# --- Sort + filter ---------------------------------------------------------


def test_sort_by_grade_orders_high_to_low_nulls_last(client, world):
    from staff import services

    rows = services.sort_and_filter(services.collect_learners(), sort="grade")
    assert [r.user.first_name for r in rows] == ["Alice", "Bob", "Carol"]


def test_filter_by_tier_narrows_the_list(client, world):
    from staff import services

    rows = services.sort_and_filter(services.collect_learners(), tier="distinction")
    assert [r.user.first_name for r in rows] == ["Alice"]


def test_learners_page_respects_the_grade_filter(client, world):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:learners") + "?filter=distinction").content.decode()
    assert "alice@example.com" in body
    assert "bob@example.com" not in body


def test_bad_sort_param_falls_back(client, world):
    client.force_login(world["admin"])
    # Does not error; just uses the default sort.
    assert client.get(reverse("staff:learners") + "?sort=drop_table").status_code == 200


# --- CSV export ------------------------------------------------------------


def test_csv_export_headers_and_rows(client, world):
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:learners_csv"))

    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    assert "attachment" in resp["Content-Disposition"]
    assert "cybaroo-learner-progress.csv" in resp["Content-Disposition"]

    text = resp.content.decode()
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert lines[0].startswith("Name,Email,Organisation")
    # One header + three learners.
    assert len(lines) == 4
    assert "alice@example.com" in text
    assert "Distinction" in text
    assert "Docklands Dental" in text
