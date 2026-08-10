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
# Tier / rank emblems (Bronze … Diamond)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "points,slug",
    [
        (0, "bronze"), (99, "bronze"),
        (100, "silver"), (219, "silver"),
        (220, "gold"), (379, "gold"),
        (380, "platinum"), (539, "platinum"),
        (540, "diamond"), (9999, "diamond"),
    ],
)
def test_tier_lands_in_the_right_band(points, slug):
    assert g.tier_for_points(points).tier.slug == slug


def test_tier_progress_points_to_next():
    t = g.tier_for_points(160)          # in Silver (100), next Gold (220)
    assert t.tier.slug == "silver"
    assert t.next_tier.slug == "gold"
    assert t.to_next == 60              # 220 - 160
    assert t.into_tier == 60            # 160 - 100
    assert t.band_span == 120           # 220 - 100
    assert t.percent == 50              # 60 / 120


def test_top_tier_is_maxed_out():
    t = g.tier_for_points(540)
    assert t.is_max is True
    assert t.next_tier is None
    assert t.to_next == 0
    assert t.percent == 100


def test_negative_points_clamp_to_bronze():
    t = g.tier_for_points(-50)
    assert t.tier.slug == "bronze"
    assert t.points == 0


def test_tier_never_decreases_as_points_rise():
    """Tier is a monotonic function of points, so it can't contradict level."""
    last = -1
    for p in range(0, 560, 7):
        idx = g.tier_for_points(p).index
        assert idx >= last
        last = idx


def test_tier_matches_points_ceiling():
    """Only a full course (all lessons + quizzes = 540) reaches Diamond."""
    assert g.tier_for_points(539).tier.slug != "diamond"
    assert g.tier_for_points(540).tier.slug == "diamond"


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
    assert "Don't break your 7-day streak" in status.message and "before midnight" in status.message


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
        "points": 0,
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
        "points": 10,
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
        "points": 0,
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


# --------------------------------------------------------------------------
# Streak milestones
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_streak_status_surfaces_the_next_milestone(student):
    profile = g.get_profile(student)
    profile.streak_count = 3
    profile.last_active = _aware(TODAY)
    profile.badges = ["streak_3"]  # earned the 3-day; next is 7
    status = g.streak_status(profile, today=TODAY)
    assert status.milestone == 7
    assert status.to_milestone == 4


@pytest.mark.django_db
def test_milestone_advances_to_30_once_7_is_earned(student):
    profile = g.get_profile(student)
    profile.streak_count = 7
    profile.last_active = _aware(TODAY)
    profile.badges = ["streak_3", "streak_7"]
    status = g.streak_status(profile, today=TODAY)
    assert status.milestone == 30
    assert status.to_milestone == 23


def test_the_new_streak_badges_evaluate_at_their_thresholds():
    from modules.badges import BY_ID

    assert BY_ID["streak_7"].evaluate({"streak": 7}) is True
    assert BY_ID["streak_7"].evaluate({"streak": 6}) is False
    assert BY_ID["streak_30"].evaluate({"streak": 30}) is True
