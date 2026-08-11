"""The Administrator dashboard's data, computed in a fixed number of queries.

Dashboards are the #1 N+1 risk here (CLAUDE.md), and the learner list crosses
every learner against every module. So instead of asking the gamification
engine per student (one round of queries each), it pulls a handful of grouped
aggregates once and composes the rows in Python. The query count does not grow
with the number of learners: it is constant.

The single-learner detail path (learner_detail) is allowed to be per-user — it
serves one person, so the engine's normal per-user helpers are exactly right.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

from django.db.models import Count, Max, Q
from django.utils import timezone

from authentication.models import User, UserProfile
from modules import badges as badge_catalogue
from modules import gamification as g
from modules.grading import BANDS, Tier, grade_from_scores, tier_for_score
from modules.models import Module, ProgressRecord, SimulationResult
from quizzes.models import Quiz, QuizResult

from .models import AdminAction

# A learner who has started but gone quiet for this many days is surfaced as
# "needs attention" (alongside anyone an admin has flagged by hand).
INACTIVE_DAYS = 14


@dataclass
class LearnerRow:
    user: User
    modules_completed: int
    modules_total: int
    overall_score: int | None  # mean best score, or None if never attempted
    tier: Tier
    last_active: datetime | None
    points: int
    level: int
    flagged: bool
    days_inactive: int | None

    @property
    def name(self):
        full = self.user.get_full_name().strip()
        return full or self.user.email

    @property
    def completion_percent(self):
        if not self.modules_total:
            return 0
        return round(self.modules_completed / self.modules_total * 100)

    @property
    def completed_course(self):
        return self.modules_total > 0 and self.modules_completed == self.modules_total

    @property
    def started(self):
        return self.points > 0 or self.last_active is not None

    @property
    def inactive(self):
        return (
            self.started
            and self.days_inactive is not None
            and self.days_inactive >= INACTIVE_DAYS
        )

    @property
    def needs_attention(self):
        return self.flagged or self.inactive


# --- Sorting -----------------------------------------------------------------
#
# Each sort names a key. None sorts last regardless of direction (a learner
# with no grade or no activity belongs at the bottom, not jumbled among real
# values), so keys lead with a has-no-value flag.

SORTS = {
    "name": lambda r: (r.name.lower(),),
    "completion": lambda r: (-r.modules_completed, r.name.lower()),
    "grade": lambda r: (r.overall_score is None, -(r.overall_score or 0), r.name.lower()),
    "activity": lambda r: (
        r.last_active is None,
        -(r.last_active.timestamp() if r.last_active else 0),
        r.name.lower(),
    ),
}
DEFAULT_SORT = "name"


def collect_learners(now=None):
    """Every Student, with progress, grade and activity. Constant query count."""
    now = now or timezone.now()

    modules = list(
        Module.objects.filter(is_published=True).annotate(
            total_lessons=Count(
                "lessons", filter=Q(lessons__is_active=True), distinct=True
            )
        )
    )
    modules_total = len(modules)

    gated = set(
        Quiz.objects.filter(is_active=True, module__in=modules).values_list(
            "module_id", flat=True
        )
    )

    lessons_map = {}
    for row in (
        ProgressRecord.objects.filter(
            lesson__is_active=True, lesson__module__is_published=True
        )
        .values("user_id", "lesson__module_id")
        .annotate(n=Count("lesson", distinct=True))
    ):
        lessons_map[(row["user_id"], row["lesson__module_id"])] = row["n"]

    passed = {
        (row["user_id"], row["quiz__module_id"])
        for row in QuizResult.objects.filter(passed=True)
        .values("user_id", "quiz__module_id")
        .distinct()
    }
    best_map = {}
    for row in QuizResult.objects.values("user_id", "quiz__module_id").annotate(
        best=Max("score")
    ):
        best_map[(row["user_id"], row["quiz__module_id"])] = row["best"]

    students = (
        User.objects.filter(role=User.Role.STUDENT)
        .select_related("profile")
        .order_by("first_name", "last_name", "email")
    )

    rows = []
    for user in students:
        completed = 0
        best_scores = []
        for m in modules:
            done = lessons_map.get((user.id, m.id), 0)
            lessons_ok = m.total_lessons > 0 and done >= m.total_lessons
            quiz_ok = m.id not in gated or (user.id, m.id) in passed
            if lessons_ok and quiz_ok:
                completed += 1
            score = best_map.get((user.id, m.id))
            if score is not None:
                best_scores.append(score)

        overall_score, tier = grade_from_scores(best_scores)
        profile = getattr(user, "profile", None)
        points = profile.points if profile else 0
        last_active = profile.last_active if profile else None
        days_inactive = (now - last_active).days if last_active else None

        rows.append(
            LearnerRow(
                user=user,
                modules_completed=completed,
                modules_total=modules_total,
                overall_score=overall_score,
                tier=tier,
                last_active=last_active,
                points=points,
                level=g.level_for_points(points).level,
                flagged=bool(profile and profile.flagged),
                days_inactive=days_inactive,
            )
        )
    return rows


def sort_and_filter(rows, *, sort=DEFAULT_SORT, tier=None):
    """Order and optionally narrow the rows for the learner table."""
    if tier:
        rows = [r for r in rows if r.tier.slug == tier]
    key = SORTS.get(sort, SORTS[DEFAULT_SORT])
    return sorted(rows, key=key)


def search_learners(rows, q):
    """Narrow rows by a free-text query over name, email and organisation.

    Operates on the already-composed rows, so search adds no queries — the
    aggregation in collect_learners() stays the single bounded pass.
    """
    q = (q or "").strip().lower()
    if not q:
        return rows
    out = []
    for r in rows:
        profile = getattr(r.user, "profile", None)
        org = (profile.organisation if profile else "") or ""
        if q in f"{r.name} {r.user.email} {org}".lower():
            out.append(r)
    return out


# Quick-filter chips: one-click predicates over a composed row. The tier keys
# double as the grade filter, so the chip bar and the grade bands stay in step.
QUICK_FILTERS = {
    "attention": ("Needs attention", lambda r: r.needs_attention),
    "completed": ("Completed", lambda r: r.completed_course),
    "not_started": ("Not started", lambda r: not r.started),
    "active": ("Active (7 days)", lambda r: r.days_inactive is not None and r.days_inactive <= 7),
    "dormant": ("Dormant (14+ days)", lambda r: r.inactive),
    "distinction": ("Distinction", lambda r: r.tier.slug == "distinction"),
    "merit": ("Merit", lambda r: r.tier.slug == "merit"),
    "pass": ("Pass", lambda r: r.tier.slug == "pass"),
    "not-yet": ("Not yet", lambda r: r.tier.slug == "not-yet"),
}
STATUS_FILTER_KEYS = ["attention", "completed", "not_started", "active", "dormant"]
GRADE_FILTER_KEYS = ["distinction", "merit", "pass", "not-yet"]


def filter_learners(rows, key):
    """Apply a single quick-filter by key (or return rows unchanged)."""
    entry = QUICK_FILTERS.get(key)
    if not entry:
        return rows
    predicate = entry[1]
    return [r for r in rows if predicate(r)]


def overview(rows):
    """Headline figures for the overview page, from the composed rows."""
    total = len(rows)
    completed_course = sum(1 for r in rows if r.completed_course)
    graded = [r.overall_score for r in rows if r.overall_score is not None]

    distribution = [
        {"tier": band, "count": sum(1 for r in rows if r.tier.slug == band.slug)}
        for band in BANDS
    ]

    attention = [r for r in rows if r.needs_attention]

    return {
        "total_learners": total,
        "completed_course": completed_course,
        "completion_rate": round(completed_course / total * 100) if total else 0,
        "average_score": round(sum(graded) / len(graded)) if graded else None,
        "not_started": sum(1 for r in rows if r.overall_score is None),
        "active_learners": sum(1 for r in rows if r.started),
        "distribution": distribution,
        "attention": attention,
        "any_started": any(r.started for r in rows),
        "organisations": organisations(rows),
    }


def organisations(rows, limit=6):
    """Learners per organisation, most populous first, for the overview chart."""
    buckets = {}
    for r in rows:
        profile = getattr(r.user, "profile", None)
        name = (profile.organisation.strip() if profile and profile.organisation else "") or "No organisation"
        b = buckets.setdefault(name, {"name": name, "count": 0, "started": 0})
        b["count"] += 1
        if r.started:
            b["started"] += 1
    ordered = sorted(buckets.values(), key=lambda b: (-b["count"], b["name"]))
    return ordered[:limit]


def _blank_org_stats():
    return {"learners": 0, "started": 0, "completed": 0, "attention": 0,
            "avg_score": None, "completion": 0}


def managed_organisations():
    """Every Organisation record with its learner stats, most populous first.

    Starts from the Organisation table (so a freshly created org with no members
    still appears) and joins the bounded learner aggregation by name. One
    collect_learners() pass; no per-org queries.
    """
    from authentication.models import Organisation

    rows = collect_learners()
    by_name = {o["name"]: o for o in organisation_rollup(rows)}
    keys = ("learners", "started", "completed", "attention", "avg_score", "completion")

    out = []
    for org in Organisation.objects.all():
        stats = by_name.get(org.name, _blank_org_stats())
        out.append({"org": org, **{k: stats[k] for k in keys}})
    out.sort(key=lambda o: (-o["learners"], o["org"].name.lower()))
    return out


def organisation_members(org):
    """The learner rows belonging to one organisation (by FK). Bounded."""
    rows = collect_learners()
    return [r for r in rows if getattr(r.user, "profile", None) and r.user.profile.org_id == org.id]


def resolve_organisation(name):
    """Get or create an Organisation for a free-text name (or None if blank)."""
    from authentication.models import Organisation

    name = (name or "").strip()
    if not name:
        return None
    org, _ = Organisation.objects.get_or_create(name=name)
    return org


def assign_learner_org(profile, org):
    """Point a learner at an organisation (or clear it), keeping the text mirror
    in step so search, the rollup and the CSV export stay correct."""
    profile.org = org
    profile.organisation = org.name if org else ""
    profile.save(update_fields=["org", "organisation"])


def organisation_rollup(rows):
    """Every organisation with aggregate stats, for the organisations view.

    Composed from the same rows as everything else, so it is still one bounded
    aggregation. Each bucket carries learner count, how many have started and
    completed, average grade, and how many need attention.
    """
    buckets = {}
    for r in rows:
        profile = getattr(r.user, "profile", None)
        name = (profile.organisation.strip() if profile and profile.organisation else "") or "No organisation"
        b = buckets.setdefault(
            name,
            {"name": name, "learners": 0, "started": 0, "completed": 0,
             "attention": 0, "_scores": []},
        )
        b["learners"] += 1
        if r.started:
            b["started"] += 1
        if r.completed_course:
            b["completed"] += 1
        if r.needs_attention:
            b["attention"] += 1
        if r.overall_score is not None:
            b["_scores"].append(r.overall_score)

    out = []
    for b in buckets.values():
        scores = b.pop("_scores")
        b["avg_score"] = round(sum(scores) / len(scores)) if scores else None
        b["completion"] = round(b["completed"] / b["learners"] * 100) if b["learners"] else 0
        out.append(b)
    out.sort(key=lambda b: (-b["learners"], b["name"].lower()))
    return out


# --- Audit log ---------------------------------------------------------------


def log_action(actor, action, summary, *, target_user=None):
    """Record one privileged action. Called by every mutating admin view."""
    return AdminAction.objects.create(
        actor=actor, action=action, target_user=target_user, summary=summary
    )


def recent_actions(limit=8):
    return list(
        AdminAction.objects.select_related("actor", "target_user")[:limit]
    )


def content_health():
    """A compact health read of the learning content, for the overview.

    A fixed handful of aggregate queries (no per-module loop): module publish
    counts, hidden lessons, question bank size, and how much content an admin has
    edited in the console (diverged from the authored source).
    """
    from django.db.models import Count

    from modules.models import Lesson
    from quizzes.models import Question

    modules = Module.objects.aggregate(
        total=Count("id"),
        published=Count("id", filter=Q(is_published=True)),
        edited=Count("id", filter=Q(admin_edited=True)),
    )
    lessons = Lesson.objects.aggregate(
        total=Count("id"),
        hidden=Count("id", filter=Q(is_active=False)),
        edited=Count("id", filter=Q(admin_edited=True)),
    )
    questions = Question.objects.aggregate(
        total=Count("id"),
        edited=Count("id", filter=Q(admin_edited=True)),
    )
    quizzes = Quiz.objects.filter(is_active=True).count()

    edited_total = modules["edited"] + lessons["edited"] + questions["edited"]
    return {
        "modules_total": modules["total"],
        "modules_published": modules["published"],
        "modules_unpublished": modules["total"] - modules["published"],
        "lessons_total": lessons["total"],
        "lessons_hidden": lessons["hidden"],
        "quizzes": quizzes,
        "questions_total": questions["total"],
        "edited_total": edited_total,
    }


# --- Analytics: weekly trends + hand-built SVG chart geometry -----------------
#
# Every chart on the overview is real data rendered as inline SVG. The geometry
# (points, paths, arcs) is computed HERE, server-side, so templates stay dumb and
# the maths is unit-tested. No JS charting library, so it is CSP-safe by
# construction and no number can be fabricated in the browser. Each trend is one
# grouped query (TruncWeek + aggregate), so the query count never grows with the
# cohort.


def _week_starts(weeks, now=None):
    """The Monday date starting each of the last `weeks` weeks, oldest first."""
    now = now or timezone.localdate()
    this_monday = now - timedelta(days=now.weekday())
    return [this_monday - timedelta(weeks=(weeks - 1 - i)) for i in range(weeks)]


def _bucket_by_week(pairs, starts):
    """Sum values into week buckets keyed by their Monday start.

    `pairs` is an iterable of (local_date, value); `starts` the ordered Mondays.
    """
    index = {monday: i for i, monday in enumerate(starts)}
    out = [0] * len(starts)
    first = starts[0]
    for day, value in pairs:
        monday = day - timedelta(days=day.weekday())
        i = index.get(monday)
        if i is not None and monday >= first:
            out[i] += value
    return out


def weekly_trends(weeks=12, now=None):
    """Real weekly series for the dashboard, each a single grouped query.

    Returns signups (cumulative learners), active (distinct learners active that
    week), completions (lessons + quiz passes that week) and avg_score (mean quiz
    score that week, carrying forward the last known value for empty weeks).
    """
    from django.db.models import Avg
    from django.db.models.functions import TruncWeek

    starts = _week_starts(weeks, now)
    window_start = timezone.make_aware(
        datetime(starts[0].year, starts[0].month, starts[0].day)
    )

    # New signups per week (students only), plus everyone who joined earlier so
    # the cumulative line starts from the real base.
    students = User.objects.filter(role=User.Role.STUDENT)
    base_before = students.filter(date_joined__lt=window_start).count()
    signup_rows = [
        (timezone.localdate(r["w"]), r["n"])
        for r in students.filter(date_joined__gte=window_start)
        .annotate(w=TruncWeek("date_joined"))
        .values("w")
        .annotate(n=Count("id"))
    ]
    weekly_new = _bucket_by_week(signup_rows, starts)
    signups, running = [], base_before
    for n in weekly_new:
        running += n
        signups.append(running)

    # Completions per week: lessons banked + quiz passes.
    lesson_rows = [
        (timezone.localdate(r["w"]), r["n"])
        for r in ProgressRecord.objects.filter(completed_at__gte=window_start)
        .annotate(w=TruncWeek("completed_at"))
        .values("w")
        .annotate(n=Count("id"))
    ]
    quiz_pass_rows = [
        (timezone.localdate(r["w"]), r["n"])
        for r in QuizResult.objects.filter(passed=True, submitted_at__gte=window_start)
        .annotate(w=TruncWeek("submitted_at"))
        .values("w")
        .annotate(n=Count("id"))
    ]
    completions = [
        a + b
        for a, b in zip(
            _bucket_by_week(lesson_rows, starts),
            _bucket_by_week(quiz_pass_rows, starts),
        )
    ]

    # Distinct active students per week (from lesson completions — the cheapest
    # honest activity signal that already carries a per-week timestamp).
    active_pairs = {}
    for r in (
        ProgressRecord.objects.filter(completed_at__gte=window_start)
        .annotate(w=TruncWeek("completed_at"))
        .values("w", "user")
        .distinct()
    ):
        day = timezone.localdate(r["w"])
        active_pairs[(day, r["user"])] = 1
    active = _bucket_by_week(
        [(day, 1) for (day, _uid) in active_pairs], starts
    )

    # Average quiz score per week; empty weeks carry the previous value forward
    # so the sparkline reads as a line, not a cliff to zero.
    score_by_week = {
        timezone.localdate(r["w"]): round(r["avg"] or 0)
        for r in QuizResult.objects.filter(submitted_at__gte=window_start)
        .annotate(w=TruncWeek("submitted_at"))
        .values("w")
        .annotate(avg=Avg("score"))
    }
    avg_score, carry = [], 0
    for monday in starts:
        if monday in score_by_week:
            carry = score_by_week[monday]
        avg_score.append(carry)

    return {
        "week_starts": starts,
        "signups": signups,
        "active": active,
        "completions": completions,
        "avg_score": avg_score,
    }


@dataclass
class Sparkline:
    line: str        # "x,y x,y …" for a <polyline>
    area: str        # closed path for the fill
    dot: tuple       # (x, y) of the latest point
    width: int
    height: int
    flat: bool       # True when there's nothing meaningful to draw


def sparkline(values, width=110, height=30, pad=3):
    """Normalise a series into SVG coordinates for a mini trend line."""
    n = len(values)
    if n == 0 or max(values) == min(values):
        y = height / 2
        line = f"{pad},{y:.1f} {width - pad},{y:.1f}"
        return Sparkline(line, "", (width - pad, y), width, height, flat=True)

    lo, hi = min(values), max(values)
    span = hi - lo
    step = (width - 2 * pad) / (n - 1) if n > 1 else 0
    pts = []
    for i, v in enumerate(values):
        x = pad + i * step
        y = height - pad - (v - lo) / span * (height - 2 * pad)
        pts.append((x, y))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = (
        f"M{pts[0][0]:.1f},{height} "
        + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts)
        + f" L{pts[-1][0]:.1f},{height} Z"
    )
    return Sparkline(line, area, pts[-1], width, height, flat=False)


@dataclass
class AreaChart:
    line: str
    area: str
    points: list      # [(x, y, value, label), …] for markers / a11y
    gridlines: list   # [(y, label), …]
    xlabels: list     # [(x, label), …]
    width: int
    height: int
    max_value: int
    empty: bool


def area_chart(values, labels, width=560, height=190, pad_l=30, pad_b=22, pad_t=12, pad_r=8):
    """Geometry for the main completions-over-time area chart."""
    n = len(values)
    peak = max(values) if values else 0
    if n == 0 or peak == 0:
        return AreaChart("", "", [], [], [], width, height, 0, empty=True)

    # A tidy y-axis top: round the peak up to a "nice" number.
    def _nice(v):
        for step in (5, 10, 20, 25, 50, 100, 200, 500, 1000):
            if v <= step:
                return step
        return (v // 1000 + 1) * 1000

    top = _nice(peak)
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    step = plot_w / (n - 1) if n > 1 else 0

    pts = []
    for i, v in enumerate(values):
        x = pad_l + i * step
        y = pad_t + (1 - v / top) * plot_h
        pts.append((x, y))

    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = (
        f"M{pad_l},{pad_t + plot_h} "
        + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts)
        + f" L{pad_l + plot_w:.1f},{pad_t + plot_h} Z"
    )

    gridlines = []
    for frac in (0, 0.5, 1):
        gy = pad_t + frac * plot_h
        gridlines.append((round(gy, 1), int(top * (1 - frac))))

    # Show a handful of x labels (first, a few middles, last) to avoid crowding.
    xlabels = []
    show = {0, n - 1, n // 3, 2 * n // 3} if n > 3 else set(range(n))
    for i in sorted(show):
        xlabels.append((round(pad_l + i * step, 1), labels[i]))

    points = [
        (round(x, 1), round(y, 1), values[i], labels[i]) for i, (x, y) in enumerate(pts)
    ]
    return AreaChart(line, area, points, gridlines, xlabels, width, height, top, empty=False)


@dataclass
class DonutSegment:
    slug: str
    label: str
    count: int
    percent: int
    dash: float       # arc length for stroke-dasharray
    offset: float     # negative cumulative offset for stroke-dashoffset
    gap: float        # remaining circumference


@dataclass
class Donut:
    segments: list
    total: int
    radius: float
    circumference: float
    stroke: int
    size: int
    empty: bool


def donut(pairs, size=168, stroke=22):
    """Build a donut from [(slug, label, count), …]. Percent-accurate arcs."""
    radius = (size - stroke) / 2
    circ = 2 * 3.141592653589793 * radius
    total = sum(c for _, _, c in pairs)
    if total == 0:
        return Donut([], 0, radius, circ, stroke, size, empty=True)

    segments, cursor = [], 0.0
    for slug, label, count in pairs:
        frac = count / total
        dash = frac * circ
        segments.append(
            DonutSegment(
                slug=slug,
                label=label,
                count=count,
                percent=round(frac * 100),
                dash=round(dash, 2),
                offset=round(-cursor, 2),
                gap=round(circ - dash, 2),
            )
        )
        cursor += dash
    return Donut(segments, total, round(radius, 2), round(circ, 2), stroke, size, empty=False)


def module_funnel():
    """Per-module cohort completion: how many students have finished each module.

    Bounded (a fixed handful of grouped queries, no per-learner loop), it shows
    where the cohort thins out across the six modules — the training product's
    most telling report.
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
    gated = set(
        Quiz.objects.filter(is_active=True, module__in=modules).values_list(
            "module_id", flat=True
        )
    )
    lessons_map = {}
    for row in (
        ProgressRecord.objects.filter(
            lesson__is_active=True, lesson__module__is_published=True
        )
        .values("user_id", "lesson__module_id")
        .annotate(n=Count("lesson", distinct=True))
    ):
        lessons_map[(row["user_id"], row["lesson__module_id"])] = row["n"]
    passed = {
        (row["user_id"], row["quiz__module_id"])
        for row in QuizResult.objects.filter(passed=True)
        .values("user_id", "quiz__module_id")
        .distinct()
    }
    student_ids = list(
        User.objects.filter(role=User.Role.STUDENT).values_list("id", flat=True)
    )
    total_students = len(student_ids)

    out = []
    for m in modules:
        completed = 0
        for uid in student_ids:
            lessons_ok = m.total_lessons > 0 and lessons_map.get((uid, m.id), 0) >= m.total_lessons
            quiz_ok = m.id not in gated or (uid, m.id) in passed
            if lessons_ok and quiz_ok:
                completed += 1
        out.append(
            {
                "module": m,
                "completed": completed,
                "total": total_students,
                "percent": round(completed / total_students * 100) if total_students else 0,
            }
        )
    return out


def overview_charts(stats, weeks=12):
    """Bundle every chart's geometry for the overview, from real data."""
    trends = weekly_trends(weeks)
    labels = [d.strftime("%-d %b") for d in trends["week_starts"]]

    donut_pairs = [
        (band["tier"].slug, band["tier"].name, band["count"])
        for band in stats["distribution"]
    ]
    if stats["not_started"]:
        donut_pairs.append(("not-started", "Not started", stats["not_started"]))

    return {
        "spark_learners": sparkline(trends["signups"]),
        "spark_active": sparkline(trends["active"]),
        "spark_completions": sparkline(trends["completions"]),
        "spark_avg": sparkline(trends["avg_score"]),
        "active_now": trends["active"][-1] if trends["active"] else 0,
        "completions_now": trends["completions"][-1] if trends["completions"] else 0,
        "completions_chart": area_chart(trends["completions"], labels),
        "grade_donut": donut(donut_pairs),
        "funnel": module_funnel(),
    }


# --- Single-learner detail ---------------------------------------------------


@dataclass
class TimelineEvent:
    when: datetime
    kind: str      # "lesson" | "quiz" | "simulation"
    label: str
    detail: str


def learner_detail(learner):
    """The full picture of one learner: progress, grades, badges, timeline.

    Per-user by design — this serves one person, so the engine's ordinary
    per-user helpers are the right tool, not the bulk aggregation above.
    """
    profile = g.get_profile(learner)
    progress = g.module_progress(learner)

    from modules.grading import best_scores_by_module

    best = best_scores_by_module(learner)
    modules_view = []
    for mp in progress:
        score = best.get(mp.module.id)
        modules_view.append(
            {
                "module": mp.module,
                "done_lessons": mp.done_lessons,
                "total_lessons": mp.total_lessons,
                "percent": mp.percent,
                "complete": mp.complete,
                "best_score": score,
                "tier": tier_for_score(score),
            }
        )

    overall_score, overall_tier = grade_from_scores(best.values())

    attempts = list(
        QuizResult.objects.filter(user=learner)
        .select_related("quiz__module")
        .order_by("-submitted_at")
    )

    earned = set(profile.badges or [])
    badges = [
        {"badge": b, "earned": b.id in earned} for b in badge_catalogue.CATALOGUE
    ]

    level = g.level_for_points(profile.points)
    stats = g.student_stats(learner)

    return {
        "learner": learner,
        "profile": profile,
        "modules": modules_view,
        "overall_score": overall_score,
        "overall_tier": overall_tier,
        "attempts": attempts,
        "badges": badges,
        "badges_earned": len(earned),
        "badges_total": len(badge_catalogue.CATALOGUE),
        "level": level,
        "streak": g.streak_status(profile),
        "stats": stats,
        "timeline": _timeline(learner),
    }


def _timeline(learner, limit=15):
    """A merged, newest-first feed of what the learner has actually done."""
    events = []

    for pr in (
        ProgressRecord.objects.filter(user=learner)
        .select_related("lesson", "lesson__module")
        .order_by("-completed_at")[:limit]
    ):
        events.append(
            TimelineEvent(
                when=pr.completed_at,
                kind="lesson",
                label=pr.lesson.title,
                detail=pr.lesson.module.title,
            )
        )

    for qr in (
        QuizResult.objects.filter(user=learner)
        .select_related("quiz__module")
        .order_by("-submitted_at")[:limit]
    ):
        outcome = "passed" if qr.passed else "did not pass"
        events.append(
            TimelineEvent(
                when=qr.submitted_at,
                kind="quiz",
                label=f"{qr.quiz.module.title} quiz",
                detail=f"{outcome} — {qr.score}%",
            )
        )

    for sr in (
        SimulationResult.objects.filter(user=learner)
        .select_related("simulation", "simulation__module")
        .order_by("-completed_at")[:limit]
    ):
        events.append(
            TimelineEvent(
                when=sr.completed_at,
                kind="simulation",
                label=f"{sr.simulation.module.title} simulation",
                detail=f"scored {sr.score} of {sr.total}",
            )
        )

    events.sort(key=lambda e: e.when, reverse=True)
    return events[:limit]
