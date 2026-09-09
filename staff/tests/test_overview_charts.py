"""The redesigned overview's data/geometry helpers: the weekly activity series,
the consolidated attention feed, the grade bars, the completion ring, and the
SVG area-chart geometry (which must degrade gracefully and never localise a
number into the markup)."""

import datetime

import pytest
from django.utils import timezone

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult
from staff import services

PASSWORD = "correct-horse-battery"


def _student(email, first, **profile):
    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="T",
        role=User.Role.STUDENT, is_verified=profile.pop("verified", True),
    )
    UserProfile.objects.create(user=u, **profile)
    return u


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)
    module = Module.objects.create(title="M1", order_index=1, is_published=True, created_by=admin)
    lesson = Lesson.objects.create(module=module, lesson_number=1, title="L1")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)
    return {"admin": admin, "module": module, "lesson": lesson, "quiz": quiz}


# --- activity_series ---------------------------------------------------------


def test_activity_series_buckets_by_week(world):
    learner = _student("a@example.com", "A")
    now = timezone.now()
    # one event 2 days ago (this week), two events ~10 days ago (last week).
    # Quiz attempts (distinct attempt numbers) let one learner log several events.
    for attempt, days in ((1, 2), (2, 10), (3, 11)):
        qr = QuizResult.objects.create(
            user=learner, quiz=world["quiz"], score=80, passed=True, attempt_number=attempt
        )
        QuizResult.objects.filter(pk=qr.pk).update(
            submitted_at=now - datetime.timedelta(days=days)
        )

    s = services.activity_series(weeks=12, now=now)
    assert len(s["values"]) == 12
    assert s["this_week"] == 1
    assert s["last_week"] == 2
    assert s["delta"] == -1
    assert s["total"] == 3
    assert s["has_data"] is True


def test_activity_series_empty_degrades(world):
    _student("a@example.com", "A")   # no activity
    s = services.activity_series()
    assert s["has_data"] is False
    assert s["this_week"] == 0 and s["delta"] == 0


# --- area_chart --------------------------------------------------------------


def test_area_chart_geometry_is_string_only():
    chart = services.area_chart([0, 1, 4, 2, 8])
    # every coordinate is a string, so nothing is number-localised into the SVG
    assert isinstance(chart["area_path"], str) and chart["area_path"].startswith("M")
    assert isinstance(chart["line_points"], str)
    assert all(isinstance(g, str) for g in chart["gridlines"])
    assert isinstance(chart["endpoint"]["x"], str) and isinstance(chart["endpoint"]["y"], str)
    assert {"width", "height", "x_left", "x_right", "y_labels", "x_labels"} <= set(chart)


def test_area_chart_handles_all_zero_without_dividing_by_zero():
    chart = services.area_chart([0, 0, 0])   # vmax guarded to 1
    assert chart["area_path"]                 # no exception, renders a flat baseline


# --- attention_feed ----------------------------------------------------------


def test_attention_feed_consolidates_and_prioritises(world):
    # one of each cohort
    not_started = _student("ns@example.com", "Ned")                                  # never started
    stalled = _student("st@example.com", "Sam", points=10,
                       last_active=timezone.now() - datetime.timedelta(days=20))       # started, quiet
    ProgressRecord.objects.create(user=stalled, lesson=world["lesson"])
    unverified = _student("uv@example.com", "Uma", verified=False)                    # not confirmed
    failing = _student("fl@example.com", "Fin", points=10,
                       last_active=timezone.now() - datetime.timedelta(days=1))
    for n in (1, 2):
        QuizResult.objects.create(user=failing, quiz=world["quiz"], score=40,
                                  passed=False, attempt_number=n)

    feed = services.attention_feed(services.collect_learners(), sample=10)
    tones = [it["tone"] for it in feed["items"]]
    # failing first, then stalled, then unverified, then not-started
    assert tones == sorted(tones, key=lambda t: {"fl": 0, "st": 1, "uv": 2, "ns": 3}[t])
    assert feed["items"][0]["tone"] == "fl"
    assert feed["total"] == 4                        # four distinct learners flagged
    assert {c["key"] for c in feed["chips"]} == {"not_started", "stalled", "repeat_failed", "unverified"}


# --- grade_bars + completion_ring -------------------------------------------


def test_grade_bars_percentages_and_totals(world):
    stats = {
        "distribution": [
            {"tier": type("T", (), {"name": "Distinction", "slug": "distinction"})(), "count": 2},
            {"tier": type("T", (), {"name": "Pass", "slug": "pass"})(), "count": 4},
        ],
        "not_started": 8,
        "total_learners": 14,
    }
    g = services.grade_bars(stats)
    assert g["graded"] == 6 and g["total"] == 14
    by_slug = {r["slug"]: r for r in g["rows"]}
    assert by_slug["not-started"]["percent"] == 100     # the largest count
    assert by_slug["distinction"]["percent"] == 25      # 2 of 8
    assert by_slug["pass"]["percent"] == 50             # 4 of 8


def test_completion_ring_dash_geometry():
    ring = services.completion_ring(0)
    assert ring["dash"] == 0.0
    half = services.completion_ring(50)
    assert 0 < half["dash"] < half["gap"]
    assert round(half["dash"] / half["gap"], 2) == 0.5


# --- cohort_engagement -------------------------------------------------------


def test_cohort_engagement_splits_students_into_four_states(world):
    # completed the course
    done = _student("done@example.com", "Dee")
    ProgressRecord.objects.create(user=done, lesson=world["lesson"])
    QuizResult.objects.create(user=done, quiz=world["quiz"], score=90, passed=True, attempt_number=1)
    # progressing: started, not finished, still active
    prog = _student("prog@example.com", "Pat", points=50, last_active=timezone.now())
    ProgressRecord.objects.create(user=prog, lesson=world["lesson"])
    # stalled: started then gone quiet
    stall = _student("stall@example.com", "Stu", points=50,
                     last_active=timezone.now() - datetime.timedelta(days=30))
    ProgressRecord.objects.create(user=stall, lesson=world["lesson"])
    # not started
    _student("new@example.com", "Nia")

    e = services.cohort_engagement(services.collect_learners())
    by_key = {s["key"]: s for s in e["segments"]}
    assert e["total"] == 4 and e["has_data"] is True
    # single-module world: one lesson done + quiz passed counts as completed.
    assert by_key["completed"]["count"] == 1
    assert by_key["progressing"]["count"] == 1
    assert by_key["stalled"]["count"] == 1
    assert by_key["not_started"]["count"] == 1
    assert sum(s["count"] for s in e["segments"]) == e["total"]


def test_cohort_engagement_empty_degrades(world):
    e = services.cohort_engagement([])
    assert e["total"] == 0 and e["has_data"] is False
    assert all(s["percent"] == 0 for s in e["segments"])


# --- activity_momentum -------------------------------------------------------


def test_activity_momentum_reads_direction():
    # last 4 weeks average clearly above the prior 4 -> picking up
    up = services.activity_momentum({"values": [1, 1, 1, 1, 5, 6, 5, 6]}, span=4)
    assert up["has_data"] and up["direction"] == "up"
    assert up["recent_avg"] > up["prior_avg"]

    down = services.activity_momentum({"values": [6, 5, 6, 5, 1, 1, 1, 1]}, span=4)
    assert down["direction"] == "down"

    steady = services.activity_momentum({"values": [4, 4, 4, 4, 4, 4, 4, 4]}, span=4)
    assert steady["direction"] == "steady"


def test_activity_momentum_needs_a_full_window():
    assert services.activity_momentum({"values": [1, 2, 3]}, span=4)["has_data"] is False
    assert services.activity_momentum({"values": [0] * 12}, span=4)["has_data"] is False
