"""The gamification engine — points, levels, streaks, badges, progress.

The one rule that keeps this honest: **records are the truth, the profile is a
cache.** ProgressRecord (lessons done) and QuizResult (quizzes passed) are the
only source of what a student has achieved. `UserProfile.points` is *recomputed*
from them on every change, never incremented — so it cannot drift, and
`rebuild_profiles` can regenerate every profile from the records at any time.

Everything a screen needs comes through here, so the ORM aggregation lives in
one place and the query counts stay bounded (dashboards are the #1 N+1 risk —
CLAUDE.md). Callers pass `today`/`now` into the streak functions for tests,
rather than us reaching for a clock-mocking library.
"""

from dataclasses import dataclass

from django.db import transaction
from django.db.models import Count, F, Q
from django.utils import timezone

from authentication.models import UserProfile
from quizzes.models import Quiz, QuizResult

from . import badges as badge_catalogue
from .models import (
    LessonTask,
    Module,
    ProgressRecord,
    Simulation,
    SimulationResult,
    TaskProgress,
)

POINTS_PER_LESSON = 40
POINTS_PER_QUIZ = 200


# --------------------------------------------------------------------------
# Levels — a pure function of points, so no `level` field is ever stored
# --------------------------------------------------------------------------
#
# XP to first REACH level L is 40·(L−1)·(L+2): 160, 400, 720, 1120, 1600, 2160…
# Early levels come quickly (level 2 after four lessons), then stretch. The course
# now has 22 lessons (Module 2 is two deep lessons rather than four) + 6 quizzes =
# 2080 XP, which lands a fully finished course in the top tier (Diamond, 2000),
# between levels 6 and 7. (Curve and economy scale together, so the number of
# lessons/quizzes behind each level is unchanged from the original 10/50 economy.)


def _points_to_reach(level):
    return 40 * (level - 1) * (level + 2)


@dataclass(frozen=True)
class Level:
    level: int
    points: int
    into_level: int      # XP earned within the current level
    level_span: int      # XP the current level spans
    to_next: int         # XP remaining to the next level
    percent: int         # progress through the current level, 0–100


def level_for_points(points):
    points = max(0, int(points))
    level = 1
    while level < 99 and points >= _points_to_reach(level + 1):
        level += 1
    floor = _points_to_reach(level)
    ceil = _points_to_reach(level + 1)
    span = ceil - floor
    into = points - floor
    return Level(
        level=level,
        points=points,
        into_level=into,
        level_span=span,
        to_next=ceil - points,
        percent=round(into / span * 100) if span else 100,
    )


# --------------------------------------------------------------------------
# Module progress + the sequential lock
# --------------------------------------------------------------------------


@dataclass
class ModuleProgress:
    module: Module
    total_lessons: int
    done_lessons: int
    complete: bool
    unlocked: bool
    percent: int


def module_progress(user):
    """Progress + lock state for every published module, in order.

    Two queries regardless of module count. The lock is computed here, once, so
    views enforce it by asking this rather than re-deriving it (and getting it
    subtly wrong) each time.
    """
    modules = list(
        Module.objects.filter(is_published=True)
        .order_by("order_index")
        .annotate(
            total_lessons=Count(
                "lessons", filter=Q(lessons__is_active=True), distinct=True
            )
        )
    )
    done_map = dict(
        ProgressRecord.objects.filter(
            user=user, lesson__is_active=True, lesson__module__is_published=True
        )
        .values_list("lesson__module")
        .annotate(n=Count("lesson", distinct=True))
    )

    # A module with an active quiz is only complete once that quiz is passed —
    # lessons teach, the quiz proves it, and the pass is what unlocks the next
    # module. Modules with no active quiz (yet) fall back to lessons-only, so
    # nothing that predates its quiz regresses. Two bounded queries, whatever
    # the module count.
    module_ids = [m.id for m in modules]
    gated_module_ids = set(
        Quiz.objects.filter(module_id__in=module_ids, is_active=True).values_list(
            "module_id", flat=True
        )
    )
    passed_module_ids = set(
        QuizResult.objects.filter(
            user=user, passed=True, quiz__module_id__in=module_ids
        ).values_list("quiz__module_id", flat=True)
    )

    # DEBUG-only review switch: in local development every module is unlocked so
    # the whole course can be walked without completing each one first. Production
    # (DEBUG=False, e.g. the test suite and any real deploy) keeps the sequential
    # lock, which the views still enforce as a 403. Remove `settings.DEBUG or` to
    # restore the lock locally.
    from django.conf import settings

    review_unlock = bool(settings.DEBUG)

    out = []
    prev_complete = True  # the first module is always unlocked
    for m in modules:
        total = m.total_lessons
        done = done_map.get(m.id, 0)
        lessons_done = total > 0 and done >= total
        quiz_passed = m.id not in gated_module_ids or m.id in passed_module_ids
        complete = lessons_done and quiz_passed
        out.append(
            ModuleProgress(
                module=m,
                total_lessons=total,
                done_lessons=done,
                complete=complete,
                unlocked=review_unlock or prev_complete,
                percent=round(done / total * 100) if total else 0,
            )
        )
        prev_complete = complete
    return out


def is_module_unlocked(user, module):
    """Whether `user` may open `module`. Views call this before serving a
    lesson or simulation — the lock is enforced in the view, never only hidden
    in a template (CLAUDE.md)."""
    for mp in module_progress(user):
        if mp.module.id == module.id:
            return mp.unlocked
    return False


@dataclass
class NextStep:
    kind: str      # "lesson" | "quiz"
    module: object
    lesson: object  # None for a quiz step


def next_step(user):
    """The single next thing to do in the journey, or None if everything's done.

    It's the first unlocked, unfinished module's lowest incomplete lesson; once a
    module's lessons are all done it's the module's quiz (which is what still
    stands between the student and completing the module). The invariant from
    module_progress guarantees a quiz exists whenever lessons are done but the
    module isn't complete."""
    for mp in module_progress(user):
        if not mp.unlocked or mp.complete:
            continue
        done_numbers = set(
            ProgressRecord.objects.filter(
                user=user, lesson__module=mp.module, lesson__is_active=True
            ).values_list("lesson__lesson_number", flat=True)
        )
        lesson = (
            mp.module.lessons.filter(is_active=True)
            .exclude(lesson_number__in=done_numbers)
            .order_by("lesson_number")
            .first()
        )
        if lesson:
            return NextStep("lesson", mp.module, lesson)
        return NextStep("quiz", mp.module, None)
    return None


def continue_target(user):
    """(module, lesson) for the next incomplete lesson, or None. Kept for callers
    that only care about lessons; the quiz step is exposed via next_step."""
    step = next_step(user)
    if step and step.kind == "lesson":
        return step.module, step.lesson
    return None


def next_in_module(user, module, *, also_done=()):
    """The next step to take *inside* one module, so a student is never left on a
    finished lesson with nowhere to go.

    The first still-incomplete active lesson, else the module's active quiz if one
    exists, else None once the module is fully done. `also_done` lets a caller
    treat extra lesson numbers as complete (e.g. the lesson being finished right
    now) so a page can label "what comes next" before the record is written.
    Scoped to one module — see next_step for the cross-module journey."""
    done_numbers = set(
        ProgressRecord.objects.filter(
            user=user, lesson__module=module, lesson__is_active=True
        ).values_list("lesson__lesson_number", flat=True)
    )
    done_numbers |= set(also_done)
    lesson = (
        module.lessons.filter(is_active=True)
        .exclude(lesson_number__in=done_numbers)
        .order_by("lesson_number")
        .first()
    )
    if lesson:
        return NextStep("lesson", module, lesson)
    if Quiz.objects.filter(module=module, is_active=True).exists():
        return NextStep("quiz", module, None)
    return None


# --------------------------------------------------------------------------
# Counts + stats
# --------------------------------------------------------------------------


def _counts(user):
    progress = module_progress(user)
    lessons_completed = sum(mp.done_lessons for mp in progress)
    modules_completed = sum(1 for mp in progress if mp.complete)
    published_modules = len(progress)

    passed_quizzes = (
        QuizResult.objects.filter(user=user, passed=True)
        .values("quiz")
        .distinct()
        .count()
    )
    simulations_completed = SimulationResult.objects.filter(user=user).count()
    perfect_simulations = SimulationResult.objects.filter(
        user=user, total__gt=0, score=F("total")
    ).count()

    return {
        "lessons_completed": lessons_completed,
        "modules_completed": modules_completed,
        "published_modules": published_modules,
        "passed_quizzes": passed_quizzes,
        "simulations_completed": simulations_completed,
        "perfect_simulations": perfect_simulations,
    }


def points_from_counts(counts):
    return (
        counts["lessons_completed"] * POINTS_PER_LESSON
        + counts["passed_quizzes"] * POINTS_PER_QUIZ
    )


def student_stats(user):
    """The full stats dict a badge (or the dashboard's nearest-reward nudge)
    reads — counts plus points and the current streak. Read-only."""
    profile = get_profile(user)
    counts = _counts(user)
    return {
        **counts,
        "points": profile.points,
        "streak": profile.streak_count,
    }


# --------------------------------------------------------------------------
# Streak
# --------------------------------------------------------------------------


def _resolve_when(today, now):
    """Return a consistent (now, today) pair.

    - both given: trusted as-is.
    - only now: today is its local date.
    - only today: build a now at midday on that date (so its local date is
      today), for tests that inject a date without a timestamp.
    - neither: the real clock.
    """
    import datetime

    if now is not None:
        return now, (today or timezone.localdate(now))
    if today is not None:
        naive = datetime.datetime.combine(today, datetime.time(12, 0))
        return timezone.make_aware(naive), today
    real = timezone.now()
    return real, timezone.localdate(real)


def _apply_streak(profile, today, now):
    """Advance the streak for activity on `today` (a Melbourne local date).

    Same day: unchanged. Yesterday: +1. Any bigger gap, or the first ever
    activity: reset to 1. `today`/`now` are passed in so tests set the date
    instead of mocking the clock.
    """
    last = timezone.localdate(profile.last_active) if profile.last_active else None
    if last is None or (today - last).days > 1:
        profile.streak_count = 1
    elif (today - last).days == 1:
        profile.streak_count += 1
    # (today - last).days == 0 → same day, leave the count alone.
    profile.last_active = now


# --------------------------------------------------------------------------
# The one write path
# --------------------------------------------------------------------------


@dataclass
class Reward:
    points: int
    level: Level
    streak: int
    new_badges: list  # list of badge_catalogue.Badge


def get_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


# --------------------------------------------------------------------------
# Derived presentation — read-only, no logic change
# --------------------------------------------------------------------------
#
# Everything below computes from data that already exists. It never writes and
# never affects awarding; it just frames the same numbers to build momentum.

# A rank title per level. Grows with level; caps at the last for higher levels.
RANKS = [
    "Cyber Aware",     # level 1
    "Cyber Alert",     # 2
    "Cyber Ready",     # 3
    "Cyber Capable",   # 4
    "Cyber Defender",  # 5
    "Cyber Guardian",  # 6
    "Cyber Sentinel",  # 7
    "Cyber Legend",    # 8+
]


def rank_for_level(level):
    return RANKS[min(max(level, 1), len(RANKS)) - 1]


# --------------------------------------------------------------------------
# Tier / rank emblems — Bronze … Diamond
# --------------------------------------------------------------------------
#
# A coarse, game-style tier the student climbs. Computed from the SAME
# profile.points that drives Level and Streak (points = lessons·40 +
# passed_quizzes·200, recomputed from records, never incremented) — so it is
# honest and can never contradict the level. Points cap at 2080 (all 22 lessons +
# 6 quizzes), and Diamond sits at 2000, so the top tier means the course is all
# but finished. Tiers are coarser than levels and both rise with points, so they
# stay consistent by construction.


@dataclass(frozen=True)
class Tier:
    slug: str        # "bronze" … "diamond" (also the CSS accent key)
    name: str
    min_points: int


TIERS = [
    Tier("bronze", "Bronze", 0),
    Tier("silver", "Silver", 200),
    Tier("gold", "Gold", 500),
    Tier("platinum", "Platinum", 1000),
    Tier("diamond", "Diamond", 2000),
]


@dataclass(frozen=True)
class TierStatus:
    tier: Tier               # the tier the student is in now
    next_tier: Tier | None   # the tier above, or None at the top
    index: int               # 0-based position of the current tier
    total: int               # how many tiers there are
    is_max: bool             # True at Diamond
    points: int              # the student's points
    into_tier: int           # points earned within the current tier's band
    band_span: int           # points the current band spans (0 at the top)
    to_next: int             # points remaining to the next tier (0 at the top)
    percent: int             # progress across the current band, 0–100


def tier_for_points(points):
    """Where the student sits on the Bronze→Diamond ladder, with progress to next."""
    points = max(0, int(points))

    index = 0
    for i, t in enumerate(TIERS):
        if points >= t.min_points:
            index = i
    tier = TIERS[index]
    is_max = index == len(TIERS) - 1
    next_tier = None if is_max else TIERS[index + 1]

    if is_max:
        into = band_span = to_next = 0
        percent = 100
    else:
        band_span = next_tier.min_points - tier.min_points
        into = points - tier.min_points
        to_next = next_tier.min_points - points
        percent = round(into / band_span * 100) if band_span else 0

    return TierStatus(
        tier=tier,
        next_tier=next_tier,
        index=index,
        total=len(TIERS),
        is_max=is_max,
        points=points,
        into_tier=into,
        band_span=band_span,
        to_next=to_next,
        percent=percent,
    )


# Streak milestones that map to real, earnable badges (streak_3/7/30).
STREAK_MILESTONES = [3, 7, 30]


@dataclass
class StreakStatus:
    state: str        # "none" | "at_risk" | "safe"
    display: int      # the number to show (0 if lapsed, so we don't lie)
    message: str
    milestone: int    # the next streak milestone target, or 0 if all reached
    to_milestone: int # days remaining to that milestone


def _next_streak_milestone(streak, earned):
    """The next unearned streak badge target and days to it, or (0, 0)."""
    earned = set(earned or [])
    for m in STREAK_MILESTONES:
        if f"streak_{m}" not in earned:
            return m, max(0, m - streak)
    return 0, 0


def streak_status(profile, today=None):
    """How the streak stands *today* — the flame, with real stakes.

    Read-only: it does not reset or advance anything (that happens on activity,
    in _apply_streak). It interprets the stored state for display, shows 0 for a
    streak that has silently lapsed rather than a stale number, and surfaces the
    next milestone badge.
    """
    today = today or timezone.localdate()
    last = timezone.localdate(profile.last_active) if profile.last_active else None
    count = profile.streak_count

    if not count or last is None:
        state, display, msg = "none", 0, "Complete a lesson today to start a streak."
    elif last == today:
        state, display = "safe", count
        msg = f"Locked in for today — see you tomorrow to make it {count + 1}."
    elif (today - last).days == 1:
        state, display = "at_risk", count
        msg = f"Don't break your {count}-day streak — finish a lesson today before midnight."
    else:
        # Older than yesterday: the next activity resets it, so it's gone.
        state, display, msg = "none", 0, "Your streak lapsed — start a fresh one today."

    milestone, to_milestone = _next_streak_milestone(display, profile.badges)
    return StreakStatus(state, display, msg, milestone, to_milestone)


def greeting(now=None):
    """A time-aware greeting, on the Melbourne clock."""
    hour = timezone.localtime(now or timezone.now()).hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


@transaction.atomic
def refresh_profile(user, *, bump_streak=False, today=None, now=None):
    """Reconcile the cached profile with the records. The single write path for
    points, streak and badges.

    Locks the profile row so two concurrent completions can't race on the badge
    list or streak. Recomputes points from truth (never +=). Returns a Reward
    describing what changed, for the celebration moment.
    """
    # Ensure the row exists before locking it — not every account is created
    # through the registration view (superusers, tests), and select_for_update
    # can only lock a row that's already there.
    UserProfile.objects.get_or_create(user=user)
    profile = UserProfile.objects.select_for_update().get(user=user)

    counts = _counts(user)
    points = points_from_counts(counts)

    if bump_streak:
        # `today` and `now` must agree: the streak compares dates but stores a
        # timestamp, and if the stored timestamp's local date differs from
        # `today`, the next day's comparison breaks. In production now=real and
        # today=its local date. When a test injects `today` alone, derive a
        # matching `now` on that date rather than defaulting to the real clock
        # (which is what silently desynced them).
        now, today = _resolve_when(today, now)
        _apply_streak(profile, today, now)

    stats = {**counts, "points": points, "streak": profile.streak_count}
    new_ids = badge_catalogue.newly_earned(stats, profile.badges)

    profile.points = points
    if new_ids:
        profile.badges = list(profile.badges) + new_ids
    profile.save(update_fields=["points", "streak_count", "last_active", "badges"])

    return Reward(
        points=points,
        level=level_for_points(points),
        streak=profile.streak_count,
        new_badges=[badge_catalogue.BY_ID[i] for i in new_ids],
    )


def complete_lesson(user, lesson, *, today=None, now=None):
    """Mark a lesson done. Idempotent: the unique(user, lesson) constraint means
    a second call creates nothing and awards nothing. Returns (created, Reward)."""
    _, created = ProgressRecord.objects.get_or_create(user=user, lesson=lesson)
    reward = refresh_profile(user, bump_streak=created, today=today, now=now)
    return created, reward


def complete_simulation(user, simulation, *, score, total, path, today=None, now=None):
    """Record a simulation outcome (overwriting any previous run) and reconcile."""
    SimulationResult.objects.update_or_create(
        user=user,
        simulation=simulation,
        defaults={"score": score, "total": total, "path": path},
    )
    return refresh_profile(user, bump_streak=True, today=today, now=now)


def record_login(user, *, today=None, now=None):
    """Showing up is activity: keep the streak and profile current on sign-in."""
    return refresh_profile(user, bump_streak=True, today=today, now=now)


# --------------------------------------------------------------------------
# Interactive lesson tasks — the XP bar, and banking the lesson on completion
# --------------------------------------------------------------------------
#
# Tasks subdivide a lesson's points for display; the economy is unchanged.
# Completing every task in a lesson banks the whole lesson through the normal
# ProgressRecord path (+POINTS_PER_LESSON), so points/levels/streaks are
# identical to a plain "mark complete" — the tasks just fill a bar on the way.


@dataclass
class TaskResult:
    task_created: bool          # False if this task was already done
    task_points: int            # this task's contribution to the lesson's XP
    lesson_points_done: int     # XP earned in this lesson so far
    lesson_points_total: int    # the lesson's total XP (sums to POINTS_PER_LESSON)
    tasks_done: int
    tasks_total: int
    lesson_completed: bool      # did THIS call finish (and bank) the lesson?
    reward: object              # Reward when the lesson just banked, else None


def lesson_task_stats(user, lesson):
    """(done_task_ids, tasks_total, points_done, points_total) for a lesson.

    One query for the tasks, one for the student's progress on them.
    """
    tasks = list(lesson.tasks.values_list("id", "points"))
    points_total = sum(p for _, p in tasks)
    done_ids = set(
        TaskProgress.objects.filter(user=user, task__lesson=lesson).values_list(
            "task_id", flat=True
        )
    )
    points_done = sum(p for tid, p in tasks if tid in done_ids)
    return done_ids, len(tasks), points_done, points_total


@transaction.atomic
def complete_task(user, task, *, today=None, now=None):
    """Record a completed task; bank the lesson once every task is done.

    Idempotent per (user, task). The lesson banks its points exactly once — the
    first time the last task lands — via complete_lesson, which creates the
    ProgressRecord and returns the celebration Reward.
    """
    _, created = TaskProgress.objects.get_or_create(user=user, task=task)
    lesson = task.lesson

    done_ids, tasks_total, points_done, points_total = lesson_task_stats(user, lesson)
    all_done = tasks_total > 0 and len(done_ids) >= tasks_total

    lesson_completed = False
    reward = None
    if all_done and not ProgressRecord.objects.filter(user=user, lesson=lesson).exists():
        lesson_completed, reward = complete_lesson(user, lesson, today=today, now=now)

    return TaskResult(
        task_created=created,
        task_points=task.points,
        lesson_points_done=points_done,
        lesson_points_total=points_total,
        tasks_done=len(done_ids),
        tasks_total=tasks_total,
        lesson_completed=lesson_completed,
        reward=reward,
    )


# --------------------------------------------------------------------------
# Activity calendar — a real month view of the days a student studied.
# --------------------------------------------------------------------------

# Activity is anything the records count as showing up: a lesson completed, a
# simulation finished, or a quiz submitted. Each carries a timestamp; we bucket
# them by *local* date (Melbourne), because that's the day the student saw. The
# `kind` labels let the calendar tooltip say *what* was done, not just how much.
_ACTIVITY_SOURCES = (
    (ProgressRecord, "completed_at", "lessons"),
    (SimulationResult, "completed_at", "simulations"),
    (QuizResult, "submitted_at", "quizzes"),
)

# Singular/plural nouns for the tooltip phrase, in the order they should read.
_ACTIVITY_NOUNS = (
    ("lessons", "lesson", "lessons"),
    ("quizzes", "quiz", "quizzes"),
    ("simulations", "simulation", "simulations"),
)


def _activity_phrase(breakdown):
    """A human tooltip clause from a per-type breakdown, e.g. "2 lessons, 1 quiz".

    Reads in a fixed order (lessons, quizzes, simulations), skips zero counts,
    and pluralises each noun. Empty for a day with nothing.
    """
    parts = []
    for key, singular, plural in _ACTIVITY_NOUNS:
        n = breakdown.get(key, 0)
        if n:
            parts.append(f"{n} {singular if n == 1 else plural}")
    return ", ".join(parts)


# Heat buckets: how many things (lessons completed / quizzes / simulations) a
# student did on a day, mapped to a 0–4 intensity for the heat-map. The unit is
# "things finished", so the gradient means real work, not mere logins.
HEAT_MAX_LEVEL = 4


def heat_level(count):
    """Map a day's activity count to a 0–4 heat level."""
    if count <= 0:
        return 0
    return min(count, HEAT_MAX_LEVEL)


@dataclass
class CalendarDay:
    date: object       # datetime.date
    day: int           # day-of-month number to print
    in_month: bool     # False for the leading/trailing days of adjacent months
    active: bool       # the student did something on this day
    count: int         # how many things they finished that day
    level: int         # 0–4 heat intensity (0 = nothing)
    is_today: bool
    breakdown: dict    # {"lessons": n, "quizzes": n, "simulations": n}
    summary: str       # "2 lessons, 1 quiz" — the tooltip clause ("" if idle)


@dataclass
class ActivityCalendar:
    year: int
    month: int
    label: str                 # "July 2026"
    weekday_names: list        # ["Mon", …, "Sun"]
    weeks: list                # list[list[CalendarDay]], Monday-first
    active_count: int          # active days within this month
    prev_year: int
    prev_month: int
    next_year: int
    next_month: int
    can_go_next: bool          # False once showing the current month (no future)


def _activity_counts_in_range(user, start_dt, end_dt):
    """local date -> {"lessons": n, "quizzes": n, "simulations": n, "total": n},
    for [start_dt, end_dt).

    One student's activity in a single month is a handful of rows, so loading the
    timestamps and bucketing in Python is both correct (honours the Melbourne
    clock at month boundaries) and cheap. `total` drives the heat-map intensity;
    the per-type counts drive the tooltip ("what did I do that day").
    """
    from collections import defaultdict

    counts = defaultdict(lambda: {"lessons": 0, "quizzes": 0, "simulations": 0, "total": 0})
    for model, field, kind in _ACTIVITY_SOURCES:
        stamps = (
            model.objects.filter(
                user=user, **{f"{field}__gte": start_dt, f"{field}__lt": end_dt}
            )
            .values_list(field, flat=True)
        )
        for stamp in stamps:
            bucket = counts[timezone.localdate(stamp)]
            bucket[kind] += 1
            bucket["total"] += 1
    return counts


def activity_calendar(user, *, year=None, month=None, today=None):
    """A traditional Monday–Sunday month grid marking the student's active days.

    Real data only: active days come from ProgressRecord / SimulationResult /
    QuizResult timestamps. `year`/`month` pick the month to show (defaulting to
    the current one); `today` is injectable for tests rather than mocking a clock.
    """
    import calendar as _calendar
    import datetime

    today = today or timezone.localdate()
    year = year or today.year
    month = month or today.month

    # A local-aware [first-of-month, first-of-next-month) window. Filtering on it
    # and converting with localdate keeps boundary timestamps in the right day.
    start_dt = timezone.make_aware(datetime.datetime(year, month, 1))
    if month == 12:
        end_dt = timezone.make_aware(datetime.datetime(year + 1, 1, 1))
    else:
        end_dt = timezone.make_aware(datetime.datetime(year, month + 1, 1))
    counts = _activity_counts_in_range(user, start_dt, end_dt)

    _empty = {"lessons": 0, "quizzes": 0, "simulations": 0, "total": 0}

    def _day(d):
        in_month = d.month == month
        bucket = counts.get(d) if in_month else None
        total = bucket["total"] if bucket else 0
        return CalendarDay(
            date=d,
            day=d.day,
            in_month=in_month,
            active=in_month and total > 0,
            count=total,
            level=heat_level(total) if in_month else 0,
            is_today=d == today,
            breakdown=bucket or dict(_empty),
            summary=_activity_phrase(bucket) if bucket else "",
        )

    cal = _calendar.Calendar(firstweekday=0)  # 0 = Monday
    weeks = [[_day(d) for d in week] for week in cal.monthdatescalendar(year, month)]

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)
    # Never page into the future — there's no activity to see there.
    can_go_next = (year, month) < (today.year, today.month)

    return ActivityCalendar(
        year=year,
        month=month,
        label=f"{_calendar.month_name[month]} {year}",
        weekday_names=list(_calendar.day_abbr),  # Mon … Sun (firstweekday=0)
        weeks=weeks,
        active_count=sum(
            1 for d, c in counts.items() if d.month == month and c["total"] > 0
        ),
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        can_go_next=can_go_next,
    )
