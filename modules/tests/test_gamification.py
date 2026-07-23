"""The gamification engine: points, levels, streaks, badges, the lock.

The theme: numbers come from records, and they can't drift or double-count.
"""

from datetime import date, timedelta

import pytest

from modules import gamification as g
from modules.models import ProgressRecord, SimulationResult

TODAY = date(2026, 7, 18)


def complete_module(student, module, *, today=TODAY):
    reward = None
    for lesson in module.lessons.order_by("lesson_number"):
        _, reward = g.complete_lesson(student, lesson, today=today)
    return reward


# --------------------------------------------------------------------------
# Levels — a pure function, easy to pin exactly
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "points,level",
    [(0, 1), (10, 1), (39, 1), (40, 2), (100, 3), (180, 4), (540, 7)],
)
def test_level_thresholds(points, level):
    assert g.level_for_points(points).level == level


def test_level_reports_progress_within_the_level():
    lv = g.level_for_points(20)  # halfway from 0 to 40
    assert lv.level == 1
    assert lv.percent == 50
    assert lv.to_next == 20


# --------------------------------------------------------------------------
# Points — from records, never incremented
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_completed_lesson_is_worth_ten_points(student, modules):
    _, reward = g.complete_lesson(student, modules[0].lessons.first())
    assert reward.points == 10


@pytest.mark.django_db
def test_completing_a_lesson_twice_awards_it_once(student, modules):
    lesson = modules[0].lessons.first()

    created_first, r1 = g.complete_lesson(student, lesson)
    created_again, r2 = g.complete_lesson(student, lesson)

    assert created_first is True
    assert created_again is False
    assert r2.points == 10
    assert ProgressRecord.objects.filter(user=student).count() == 1


@pytest.mark.django_db
def test_points_are_recomputed_from_records_not_incremented(student, modules):
    """The cache is rewritten from the records, so a stray edit to the stored
    value is corrected on the next reconcile rather than compounding."""
    complete_module(student, modules[0])  # 4 lessons → 40
    profile = g.get_profile(student)
    assert profile.points == 40

    profile.points = 9999  # simulate drift
    profile.save(update_fields=["points"])

    g.refresh_profile(student)
    profile.refresh_from_db()
    assert profile.points == 40


# --------------------------------------------------------------------------
# The sequential lock
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_first_module_is_unlocked_and_the_second_is_not(student, modules):
    assert g.is_module_unlocked(student, modules[0]) is True
    assert g.is_module_unlocked(student, modules[1]) is False


@pytest.mark.django_db
def test_finishing_a_module_unlocks_the_next(student, modules):
    complete_module(student, modules[0])
    assert g.is_module_unlocked(student, modules[1]) is True
    assert g.is_module_unlocked(student, modules[2]) is False


@pytest.mark.django_db
def test_a_partly_done_module_does_not_unlock_the_next(student, modules):
    # three of four lessons
    for lesson in modules[0].lessons.order_by("lesson_number")[:3]:
        g.complete_lesson(student, lesson)
    assert g.is_module_unlocked(student, modules[1]) is False


@pytest.mark.django_db
def test_module_progress_percentages(student, modules):
    for lesson in modules[0].lessons.order_by("lesson_number")[:2]:
        g.complete_lesson(student, lesson)

    first = g.module_progress(student)[0]
    assert first.done_lessons == 2
    assert first.total_lessons == 4
    assert first.percent == 50
    assert first.complete is False


@pytest.mark.django_db
def test_continue_target_is_the_next_incomplete_lesson(student, modules):
    g.complete_lesson(student, modules[0].lessons.get(lesson_number=1))

    module, lesson = g.continue_target(student)
    assert module.order_index == 1
    assert lesson.lesson_number == 2


@pytest.mark.django_db
def test_continue_target_is_none_when_everything_is_done(student, make_module):
    module = make_module(1, lessons=2)
    complete_module(student, module)
    assert g.continue_target(student) is None


# --------------------------------------------------------------------------
# Streak — dates injected, no clock mocking
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_first_activity_starts_a_one_day_streak(student, modules):
    reward = g.complete_lesson(student, modules[0].lessons.first(), today=TODAY)[1]
    assert reward.streak == 1


@pytest.mark.django_db
def test_activity_on_consecutive_days_extends_the_streak(student, modules):
    lessons = list(modules[0].lessons.order_by("lesson_number"))
    g.complete_lesson(student, lessons[0], today=TODAY)
    r = g.complete_lesson(student, lessons[1], today=TODAY + timedelta(days=1))[1]
    assert r.streak == 2


@pytest.mark.django_db
def test_same_day_activity_does_not_double_count_the_streak(student, modules):
    lessons = list(modules[0].lessons.order_by("lesson_number"))
    g.complete_lesson(student, lessons[0], today=TODAY)
    r = g.complete_lesson(student, lessons[1], today=TODAY)[1]
    assert r.streak == 1


@pytest.mark.django_db
def test_a_gap_resets_the_streak(student, modules):
    lessons = list(modules[0].lessons.order_by("lesson_number"))
    g.complete_lesson(student, lessons[0], today=TODAY)
    r = g.complete_lesson(student, lessons[1], today=TODAY + timedelta(days=3))[1]
    assert r.streak == 1


# --------------------------------------------------------------------------
# Badges — earned once, only when earned
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_first_lesson_earns_the_first_step_badge(student, modules):
    reward = g.complete_lesson(student, modules[0].lessons.first())[1]
    ids = [b.id for b in reward.new_badges]
    assert "first_lesson" in ids


@pytest.mark.django_db
def test_a_badge_is_only_announced_the_once(student, modules):
    lessons = list(modules[0].lessons.order_by("lesson_number"))
    first = g.complete_lesson(student, lessons[0])[1]
    second = g.complete_lesson(student, lessons[1])[1]

    assert "first_lesson" in [b.id for b in first.new_badges]
    assert "first_lesson" not in [b.id for b in second.new_badges]
    # still held, just not re-announced
    assert "first_lesson" in g.get_profile(student).badges


@pytest.mark.django_db
def test_finishing_all_modules_earns_the_graduate_badge(student, make_module):
    a = make_module(1, lessons=1)
    b = make_module(2, lessons=1)
    complete_module(student, a)
    reward = complete_module(student, b)
    assert "graduate" in g.get_profile(student).badges


@pytest.mark.django_db
def test_a_perfect_simulation_earns_the_sharp_eye_badge(student, modules):
    sim = modules[0].simulation
    g.complete_simulation(student, sim, score=1, total=1, path=[{"id": "a", "ok": True}])

    earned = g.get_profile(student).badges
    assert "first_simulation" in earned
    assert "sharp_eye" in earned
    assert SimulationResult.objects.filter(user=student, simulation=sim).count() == 1


@pytest.mark.django_db
def test_an_imperfect_simulation_does_not_earn_sharp_eye(student, modules):
    g.complete_simulation(
        student, modules[0].simulation, score=1, total=2, path=[]
    )
    earned = g.get_profile(student).badges
    assert "first_simulation" in earned
    assert "sharp_eye" not in earned


# --------------------------------------------------------------------------
# Query budget — the dashboard's #1 risk is N+1
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_module_progress_is_a_fixed_number_of_queries(student, make_module, django_assert_max_num_queries):
    for i in range(1, 7):
        make_module(i)
    # Two queries regardless of how many modules exist.
    with django_assert_max_num_queries(2):
        g.module_progress(student)


# --------------------------------------------------------------------------
# Activity calendar — a real month view of the days a student studied
# --------------------------------------------------------------------------

import datetime

from django.utils import timezone


def _study_on(student, module, lesson_number, when):
    """Record a completed lesson and stamp it onto a specific local date.

    completed_at is auto_now_add (real clock), so we create the row then force
    the date the way real activity would have landed it.
    """
    lesson = module.lessons.get(lesson_number=lesson_number)
    record = ProgressRecord.objects.create(user=student, lesson=lesson)
    aware = timezone.make_aware(datetime.datetime.combine(when, datetime.time(12, 0)))
    ProgressRecord.objects.filter(pk=record.pk).update(completed_at=aware)


@pytest.mark.django_db
def test_calendar_defaults_to_the_current_month(student, modules):
    today = datetime.date(2026, 7, 24)
    cal = g.activity_calendar(student, today=today)
    assert cal.year == 2026 and cal.month == 7
    assert cal.label == "July 2026"


@pytest.mark.django_db
def test_calendar_is_a_monday_first_grid_with_full_weeks(student, modules):
    cal = g.activity_calendar(student, year=2026, month=7, today=datetime.date(2026, 7, 24))
    assert cal.weekday_names == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # July 2026 starts on a Wednesday, so the first row's Mon/Tue spill from June.
    assert all(len(week) == 7 for week in cal.weeks)
    first = cal.weeks[0]
    assert (first[0].day, first[0].in_month) == (29, False)
    assert (first[2].day, first[2].in_month) == (1, True)


@pytest.mark.django_db
def test_active_days_are_marked_from_real_records(student, modules):
    _study_on(student, modules[0], 1, datetime.date(2026, 7, 3))
    _study_on(student, modules[0], 2, datetime.date(2026, 7, 3))  # same day, still one
    _study_on(student, modules[0], 3, datetime.date(2026, 7, 15))

    cal = g.activity_calendar(student, year=2026, month=7, today=datetime.date(2026, 7, 24))
    active = {d.day for week in cal.weeks for d in week if d.active}
    assert active == {3, 15}
    assert cal.active_count == 2


@pytest.mark.django_db
def test_activity_counts_simulations_and_quizzes_too(student, modules):
    from quizzes.models import Quiz, QuizResult

    # A simulation on the 5th.
    sr = SimulationResult.objects.create(
        user=student, simulation=modules[0].simulation, score=1, total=1, path=[]
    )
    SimulationResult.objects.filter(pk=sr.pk).update(
        completed_at=timezone.make_aware(datetime.datetime(2026, 7, 5, 9, 0))
    )
    # A quiz on the 9th.
    quiz = Quiz.objects.create(module=modules[0])
    qr = QuizResult.objects.create(user=student, quiz=quiz, score=80, passed=True)
    QuizResult.objects.filter(pk=qr.pk).update(
        submitted_at=timezone.make_aware(datetime.datetime(2026, 7, 9, 9, 0))
    )

    cal = g.activity_calendar(student, year=2026, month=7, today=datetime.date(2026, 7, 24))
    active = {d.day for week in cal.weeks for d in week if d.active}
    assert active == {5, 9}


@pytest.mark.django_db
def test_only_the_chosen_month_is_counted(student, modules):
    _study_on(student, modules[0], 1, datetime.date(2026, 6, 30))
    _study_on(student, modules[0], 2, datetime.date(2026, 7, 15))
    _study_on(student, modules[0], 3, datetime.date(2026, 8, 1))

    cal = g.activity_calendar(student, year=2026, month=7, today=datetime.date(2026, 7, 24))
    assert cal.active_count == 1
    assert {d.day for week in cal.weeks for d in week if d.active} == {15}


@pytest.mark.django_db
def test_today_is_flagged_only_in_its_own_month(student, modules):
    today = datetime.date(2026, 7, 24)
    this_month = g.activity_calendar(student, year=2026, month=7, today=today)
    todays = [d for week in this_month.weeks for d in week if d.is_today]
    assert len(todays) == 1 and todays[0].day == 24

    other = g.activity_calendar(student, year=2026, month=6, today=today)
    assert not any(d.is_today for week in other.weeks for d in week)


@pytest.mark.django_db
def test_navigation_targets_wrap_the_year_and_never_go_past_this_month(student, modules):
    today = datetime.date(2026, 7, 24)

    current = g.activity_calendar(student, year=2026, month=7, today=today)
    assert (current.prev_year, current.prev_month) == (2026, 6)
    assert (current.next_year, current.next_month) == (2026, 8)
    assert current.can_go_next is False  # this month — no future to page into

    past = g.activity_calendar(student, year=2026, month=3, today=today)
    assert past.can_go_next is True

    january = g.activity_calendar(student, year=2026, month=1, today=today)
    assert (january.prev_year, january.prev_month) == (2025, 12)
