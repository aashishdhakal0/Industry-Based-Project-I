"""Derived presentation helpers — rank, streak status, nearest reward, greeting.

These read the real data and frame it; they never write. Each is a pure-ish
function, so they're pinned exactly.
"""

import datetime

import pytest
from django.utils import timezone

from modules import badges as badge_catalogue
from modules import gamification as g

TODAY = datetime.date(2026, 7, 20)


# --------------------------------------------------------------------------
# Rank
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "level,rank",
    [(1, "Cyber Aware"), (5, "Cyber Defender"), (6, "Cyber Guardian"), (7, "Cyber Sentinel")],
)
def test_rank_grows_with_level(level, rank):
    assert g.rank_for_level(level) == rank


def test_rank_caps_at_the_top():
    assert g.rank_for_level(20) == "Cyber Legend"


# --------------------------------------------------------------------------
# Streak status — the emotional flame
# --------------------------------------------------------------------------


def _aware(date):
    return timezone.make_aware(datetime.datetime.combine(date, datetime.time(12, 0)))


@pytest.mark.django_db
def test_no_streak_reads_as_none(student):
    profile = g.get_profile(student)
    status = g.streak_status(profile, today=TODAY)
    assert status.state == "none"
    assert status.display == 0


@pytest.mark.django_db
def test_active_today_is_safe(student):
    profile = g.get_profile(student)
    profile.streak_count = 5
    profile.last_active = _aware(TODAY)
    status = g.streak_status(profile, today=TODAY)
    assert status.state == "safe"
    assert status.display == 5


@pytest.mark.django_db
def test_active_yesterday_is_at_risk(student):
    profile = g.get_profile(student)
    profile.streak_count = 7
    profile.last_active = _aware(TODAY - datetime.timedelta(days=1))
    status = g.streak_status(profile, today=TODAY)
    assert status.state == "at_risk"
    assert status.display == 7
    assert "keep your 7-day streak" in status.message


@pytest.mark.django_db
def test_a_lapsed_streak_shows_zero_not_a_stale_number(student):
    profile = g.get_profile(student)
    profile.streak_count = 9  # stored but stale
    profile.last_active = _aware(TODAY - datetime.timedelta(days=4))
    status = g.streak_status(profile, today=TODAY)
    assert status.state == "none"
    assert status.display == 0  # honest, not 9


# --------------------------------------------------------------------------
# Nearest reward — anticipation
# --------------------------------------------------------------------------


def test_a_brand_new_student_is_one_lesson_from_the_first_badge():
    stats = {
        "lessons_completed": 0,
        "modules_completed": 0,
        "published_modules": 6,
        "streak": 0,
    }
    result = badge_catalogue.nearest_unearned(stats, [])
    assert result is not None
    badge, phrase = result
    assert badge.id == "first_lesson"
    assert phrase == "1 lesson from your first badge"


def test_nearest_reward_prefers_the_closest():
    # First lesson done, on a 2-day streak: the 3-day streak badge (1 day away)
    # should beat finishing a whole module (4 lessons away).
    stats = {
        "lessons_completed": 1,
        "modules_completed": 0,
        "published_modules": 6,
        "streak": 2,
    }
    badge, phrase = badge_catalogue.nearest_unearned(stats, ["first_lesson"])
    assert badge.id == "streak_3"
    assert "1 day from" in phrase


def test_nearest_reward_skips_earned_badges():
    stats = {
        "lessons_completed": 0,
        "modules_completed": 0,
        "published_modules": 6,
        "streak": 0,
    }
    # If first_lesson is already held, it shouldn't be suggested.
    result = badge_catalogue.nearest_unearned(stats, ["first_lesson"])
    if result:
        assert result[0].id != "first_lesson"


# --------------------------------------------------------------------------
# Greeting
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "hour,expected",
    [(8, "Good morning"), (13, "Good afternoon"), (20, "Good evening")],
)
def test_greeting_is_time_aware(hour, expected):
    now = timezone.make_aware(datetime.datetime(2026, 7, 20, hour, 0))
    assert g.greeting(now) == expected
