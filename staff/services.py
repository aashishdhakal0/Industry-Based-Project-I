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
    repeat_failed: bool = False

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

    @property
    def is_verified(self):
        return self.user.is_verified

    @property
    def awaiting_verification(self):
        """A student account that has not yet confirmed its email."""
        return self.is_student and not self.user.is_verified

    @property
    def stalled(self):
        """Started the course, not finished it, and gone quiet — the learner who
        needs a nudge (distinct from someone who has never begun)."""
        return self.is_student and self.started and not self.completed_course and self.inactive

    @property
    def is_student(self):
        return self.user.role == User.Role.STUDENT

    @property
    def role_label(self):
        return self.user.get_role_display()

    @property
    def status(self):
        """A progress status slug for the pill: staff (non-learner) / completed /
        progress / not_started."""
        if not self.is_student:
            return "staff"
        if self.completed_course:
            return "completed"
        if self.started:
            return "progress"
        return "not_started"

    @property
    def status_label(self):
        return {
            "staff": "Staff",
            "completed": "Completed",
            "progress": "In progress",
            "not_started": "Not started",
        }[self.status]


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


def collect_learners(now=None, roles=None, as_at=None):
    """Every user in `roles`, with progress, grade and activity. Constant query
    count. Defaults to Students only (what every existing caller wants); the
    org-grouped learners view passes the staff roles too, so admins show up in
    their organisation. Non-students carry empty progress — the UI shows them as
    staff, not as never-started learners.

    `as_at` (a datetime) computes everything *as it stood on that date*: only
    lessons completed and quizzes submitted at or before it count. This is what
    the compliance report needs to answer "who had finished by 30 June".
    """
    now = now or timezone.now()
    roles = roles or (User.Role.STUDENT,)

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

    lesson_qs = ProgressRecord.objects.filter(
        lesson__is_active=True, lesson__module__is_published=True
    )
    quiz_qs = QuizResult.objects.all()
    if as_at is not None:
        lesson_qs = lesson_qs.filter(completed_at__lte=as_at)
        quiz_qs = quiz_qs.filter(submitted_at__lte=as_at)

    lessons_map = {}
    for row in (
        lesson_qs.values("user_id", "lesson__module_id")
        .annotate(n=Count("lesson", distinct=True))
    ):
        lessons_map[(row["user_id"], row["lesson__module_id"])] = row["n"]

    passed = {
        (row["user_id"], row["quiz__module_id"])
        for row in quiz_qs.filter(passed=True)
        .values("user_id", "quiz__module_id")
        .distinct()
    }
    best_map = {}
    for row in quiz_qs.values("user_id", "quiz__module_id").annotate(
        best=Max("score")
    ):
        best_map[(row["user_id"], row["quiz__module_id"])] = row["best"]

    # Repeat quiz-failers: two or more failed attempts on a module they still
    # have not passed. One bounded aggregate; the query count stays constant.
    repeat_fail_ids = set()
    for row in (
        QuizResult.objects.filter(passed=False)
        .values("user_id", "quiz__module_id")
        .annotate(n=Count("id"))
    ):
        key = (row["user_id"], row["quiz__module_id"])
        if row["n"] >= 2 and key not in passed:
            repeat_fail_ids.add(row["user_id"])

    students = (
        User.objects.filter(role__in=roles)
        .select_related("profile", "profile__org")
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
                repeat_failed=user.id in repeat_fail_ids,
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
    "not_started": ("Not started", lambda r: r.is_student and not r.started),
    "in_progress": ("In progress", lambda r: r.is_student and r.started and not r.completed_course),
    "completed": ("Completed", lambda r: r.completed_course),
    "attention": ("Needs attention", lambda r: r.needs_attention),
    "stalled": ("Stalled mid-course", lambda r: r.stalled),
    "repeat_failed": ("Repeat quiz fails", lambda r: r.is_student and r.repeat_failed),
    "unverified": ("Awaiting verification", lambda r: r.awaiting_verification),
    "active": ("Active (7 days)", lambda r: r.days_inactive is not None and r.days_inactive <= 7),
    "dormant": ("Dormant (14+ days)", lambda r: r.inactive),
    "distinction": ("Distinction", lambda r: r.tier.slug == "distinction"),
    "merit": ("Merit", lambda r: r.tier.slug == "merit"),
    "pass": ("Pass", lambda r: r.tier.slug == "pass"),
    "not-yet": ("Not yet", lambda r: r.tier.slug == "not-yet"),
}
STATUS_FILTER_KEYS = ["not_started", "in_progress", "stalled", "completed",
                      "attention", "repeat_failed", "unverified", "dormant"]
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


# --- Trends over time and the attention cohorts ------------------------------


def period_metrics(now=None, days=7):
    """Movement over the last `days`, each compared with the `days` before it,
    so the overview shows direction, not just a static number. A fixed handful of
    bounded aggregates: active learners, new sign-ups, and learning events (a
    lesson completed or a quiz submitted)."""
    now = now or timezone.now()
    cur_start = now - timedelta(days=days)
    prev_start = now - timedelta(days=2 * days)

    def _delta(cur, prev):
        return {"current": cur, "previous": prev, "delta": cur - prev}

    def _events(start, end):
        return (
            ProgressRecord.objects.filter(
                completed_at__gte=start, completed_at__lt=end
            ).count()
            + QuizResult.objects.filter(
                submitted_at__gte=start, submitted_at__lt=end
            ).count()
        )

    def _active(start, end):
        pr = set(
            ProgressRecord.objects.filter(
                completed_at__gte=start, completed_at__lt=end
            ).values_list("user_id", flat=True)
        )
        qr = set(
            QuizResult.objects.filter(
                submitted_at__gte=start, submitted_at__lt=end
            ).values_list("user_id", flat=True)
        )
        return len(pr | qr)

    def _signups(start, end):
        return User.objects.filter(
            role=User.Role.STUDENT, date_joined__gte=start, date_joined__lt=end
        ).count()

    active = _delta(_active(cur_start, now), _active(prev_start, cur_start))
    signups = _delta(_signups(cur_start, now), _signups(prev_start, cur_start))
    events = _delta(_events(cur_start, now), _events(prev_start, cur_start))
    return {
        "days": days,
        "active": active,
        "signups": signups,
        "events": events,
        # A labelled list for the template to iterate.
        "metrics": [
            {"label": "Active learners", **active},
            {"label": "New sign-ups", **signups},
            {"label": "Lessons + quizzes", **events},
        ],
    }


# The four cohorts an administrator actually chases, each linking to the matching
# learner-list quick-filter so "view all" lands on exactly this group.
_COHORTS = [
    ("not_started", "Not started", "have an account but have never begun"),
    ("stalled", "Stalled mid-course", "started, then went quiet for 14 days or more"),
    ("repeat_failed", "Failing a quiz", "failed the same quiz twice or more without passing"),
    ("unverified", "Awaiting verification", "have not confirmed their email yet"),
]


def attention_cohorts(rows, sample=6):
    """The 'what needs your attention today' groups, from the composed rows."""
    students = [r for r in rows if r.is_student]
    out = []
    for key, label, note in _COHORTS:
        predicate = QUICK_FILTERS[key][1]
        members = [r for r in students if predicate(r)]
        members.sort(key=lambda r: r.name.lower())
        out.append(
            {
                "key": key,
                "label": label,
                "note": note,
                "count": len(members),
                "sample": members[:sample],
                "more": max(0, len(members) - sample),
            }
        )
    return out


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

    today = timezone.localdate()
    out = []
    for org in Organisation.objects.all():
        stats = by_name.get(org.name, _blank_org_stats())
        row = {"org": org, **{k: stats[k] for k in keys}}
        # Overdue: the due date has passed and not everyone has finished.
        row["overdue"] = bool(
            org.training_due
            and org.training_due < today
            and row["completed"] < row["learners"]
        )
        out.append(row)
    # Overdue organisations float to the top, then by size.
    out.sort(key=lambda o: (not o["overdue"], -o["learners"], o["org"].name.lower()))
    return out


# Everyone the org surfaces list — students plus staff, so an org shows its
# administrators alongside its learners.
ALL_PEOPLE_ROLES = (User.Role.STUDENT, User.Role.INSTRUCTOR, User.Role.ADMINISTRATOR)


def organisation_members(org):
    """Every person (students + staff) belonging to one organisation. Bounded."""
    rows = collect_learners(roles=ALL_PEOPLE_ROLES)
    return [r for r in rows if getattr(r.user, "profile", None) and r.user.profile.org_id == org.id]


def unassigned_members():
    """Every person with no organisation — the 'No organisation' group."""
    rows = collect_learners(roles=ALL_PEOPLE_ROLES)
    return [r for r in rows if not getattr(getattr(r.user, "profile", None), "org_id", None)]


def group_by_organisation(rows):
    """Group composed rows into organisation sections for the grouped learners
    view. Real orgs first (A–Z), then a 'No organisation' bucket. Each section
    carries member/student counts and average completion. Pure Python over the
    rows — no extra queries."""
    buckets = {}
    for r in rows:
        profile = getattr(r.user, "profile", None)
        org_id = getattr(profile, "org_id", None)
        name = (profile.organisation.strip() if profile and profile.organisation else "")
        if org_id:
            key, display, link = ("id", org_id), name or "Organisation", org_id
        elif name:
            key, display, link = ("nm", name.lower()), name, None
        else:
            key, display, link = ("none",), "No organisation", None
        b = buckets.setdefault(
            key, {"name": display, "org_id": link, "members": [], "is_none": key == ("none",)}
        )
        b["members"].append(r)

    out = []
    for b in buckets.values():
        students = [m for m in b["members"] if m.is_student]
        completed = sum(1 for m in students if m.completed_course)
        avg = round(sum(m.completion_percent for m in students) / len(students)) if students else 0
        out.append(
            {
                **b,
                "count": len(b["members"]),
                "students": len(students),
                "completed": completed,
                "avg_completion": avg,
            }
        )
    out.sort(key=lambda g: (g["is_none"], g["name"].lower()))
    return out


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


def filter_admin_actions(params):
    """Apply the audit-log filters from a querystring, returning the narrowed
    queryset plus the active filter values (so the form can re-show them).

    Filters: actor (id), action kind, a date range over the local day, and a
    free-text search across the summary and both parties' emails. All bounded and
    indexed; shared by the log page and its CSV export so they never diverge.
    """
    import datetime as _dt

    qs = AdminAction.objects.select_related("actor", "target_user")
    active = {"actor": "", "kind": "", "q": "", "from": "", "to": ""}

    actor = (params.get("actor") or "").strip()
    if actor.isdigit():
        qs = qs.filter(actor_id=int(actor))
        active["actor"] = actor

    kind = (params.get("kind") or "").strip()
    if kind in AdminAction.Kind.values:
        qs = qs.filter(action=kind)
        active["kind"] = kind

    q = (params.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(summary__icontains=q)
            | Q(actor__email__icontains=q)
            | Q(target_user__email__icontains=q)
        )
        active["q"] = q

    def _date(name):
        raw = (params.get(name) or "").strip()
        try:
            return _dt.date.fromisoformat(raw), raw
        except ValueError:
            return None, ""

    d_from, raw_from = _date("from")
    if d_from:
        qs = qs.filter(created_at__date__gte=d_from)
        active["from"] = raw_from
    d_to, raw_to = _date("to")
    if d_to:
        qs = qs.filter(created_at__date__lte=d_to)
        active["to"] = raw_to

    return qs, active


def audit_actors():
    """Administrators who appear as an actor in the log, for the filter dropdown."""
    return list(
        User.objects.filter(admin_actions__isnull=False)
        .distinct()
        .order_by("first_name", "last_name", "email")
    )


# --- Bulk invite (onboarding a whole workplace at once) ----------------------

import re as _re

_EMAIL_TOKEN = _re.compile(r"[^@\s,;<>()\[\]\"']+@[^@\s,;<>()\[\]\"']+")


def parse_emails(text):
    """Pull every email-looking token out of pasted text or an uploaded CSV.

    Deliberately forgiving: one per line, comma/semicolon/space separated, or a
    'Name <email>' pair all work, so an admin can paste a staff list however they
    have it. Lower-cased; order preserved; de-duplicated by the caller.
    """
    return [m.group(0).strip().lower() for m in _EMAIL_TOKEN.finditer(text or "")]


def classify_invites(emails):
    """Sort a list of emails into new / already-registered / invalid, de-duped.

    One bounded query for the existing set; the rest is Python. Returns three
    ordered, unique lists so the preview can show exactly what will happen.
    """
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    cleaned = []
    seen = set()
    for e in emails:
        e = (e or "").strip().lower()
        if e and e not in seen:
            seen.add(e)
            cleaned.append(e)

    existing = set(
        User.objects.filter(email__in=cleaned).values_list("email", flat=True)
    )

    new, already, invalid = [], [], []
    for e in cleaned:
        try:
            validate_email(e)
        except ValidationError:
            invalid.append(e)
            continue
        (already if e in existing else new).append(e)
    return {"new": new, "existing": already, "invalid": invalid}


# --- Reporting: compliance + certificate register ----------------------------


def compliance_report(as_at=None, org=None):
    """Who has completed the course as at a chosen date. The compliance officer's
    core question ("prove staff finished by the deadline"). One bounded pass with
    the `as_at` cutoff; optionally scoped to one organisation.

    When the organisation has a training due date, anyone not complete is flagged
    overdue if that due date has already passed.
    """
    rows = collect_learners(as_at=as_at)
    if org is not None:
        rows = [r for r in rows if getattr(r.user, "profile", None) and r.user.profile.org_id == org.id]
    rows.sort(key=lambda r: (not r.completed_course, r.name.lower()))

    total = len(rows)
    completed = sum(1 for r in rows if r.completed_course)

    due = org.training_due if org else None
    overdue = False
    if due is not None:
        cutoff = as_at.date() if as_at is not None else timezone.localdate()
        overdue = due < cutoff

    return {
        "rows": rows,
        "total": total,
        "completed": completed,
        "not_completed": total - completed,
        "rate": round(completed / total * 100) if total else 0,
        "as_at": as_at,
        "org": org,
        "due": due,
        "past_due": overdue,
    }


def certificate_register(status=None):
    """Every certificate on the platform, newest first, for the register.

    Bounded: one query with the holder and organisation joined. `status` narrows
    to valid or revoked.
    """
    from certificates.models import Certificate

    qs = Certificate.objects.select_related("user", "user__profile", "user__profile__org")
    if status == "valid":
        qs = qs.filter(revoked_at__isnull=True)
    elif status == "revoked":
        qs = qs.filter(revoked_at__isnull=False)
    return list(qs.order_by("-issued_at"))


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




# --- Admin activity calendar (no charts) -------------------------------------
#
# A month grid marking days with platform activity: learner lesson/quiz
# completions plus administrator actions. A handful of bounded queries per
# month; timestamps are read on the Melbourne clock.


def admin_calendar(year=None, month=None, today=None):
    import calendar as _calendar
    import datetime
    from collections import Counter

    from modules.models import ProgressRecord as _PR
    from quizzes.models import QuizResult as _QR

    today = today or timezone.localdate()
    year = year or today.year
    month = month or today.month

    start_dt = timezone.make_aware(datetime.datetime(year, month, 1))
    if month == 12:
        end_dt = timezone.make_aware(datetime.datetime(year + 1, 1, 1))
    else:
        end_dt = timezone.make_aware(datetime.datetime(year, month + 1, 1))

    counts = Counter()
    for model, field in ((_PR, "completed_at"), (_QR, "submitted_at"), (AdminAction, "created_at")):
        for stamp in model.objects.filter(
            **{f"{field}__gte": start_dt, f"{field}__lt": end_dt}
        ).values_list(field, flat=True):
            counts[timezone.localdate(stamp)] += 1

    cal = _calendar.Calendar(firstweekday=0)
    weeks = [
        [
            {
                "date": d,
                "day": d.day,
                "in_month": d.month == month,
                "count": counts.get(d, 0) if d.month == month else 0,
                "active": d.month == month and counts.get(d, 0) > 0,
                "is_today": d == today,
            }
            for d in week
        ]
        for week in cal.monthdatescalendar(year, month)
    ]

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)
    return {
        "year": year,
        "month": month,
        "label": f"{_calendar.month_name[month]} {year}",
        "weekday_names": list(_calendar.day_abbr),
        "weeks": weeks,
        "active_days": sum(1 for d, c in counts.items() if d.month == month and c > 0),
        "total_events": sum(c for d, c in counts.items() if d.month == month),
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
        "can_go_next": (year, month) < (today.year, today.month),
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

    from certificates.models import Certificate

    from .models import LearnerNote

    notes = list(
        LearnerNote.objects.filter(learner=learner).select_related("author")
    )
    certificate = Certificate.objects.filter(user=learner).order_by("-issued_at").first()

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
        "notes": notes,
        "certificate": certificate,
    }


# --- Resets (audited remediation) --------------------------------------------


def reset_quiz_attempts(learner, module):
    """Delete every quiz attempt this learner has on one module, then reconcile
    the cached points/badges from the records. Returns how many were removed."""
    deleted, _ = QuizResult.objects.filter(
        user=learner, quiz__module=module
    ).delete()
    g.refresh_profile(learner)
    return deleted


def reset_module_progress(learner, module):
    """Wipe a learner's progress on one module: its lesson records, task
    progress, quiz attempts and simulation results, then reconcile the cache.
    A remediation tool (let someone start a module again), always audited."""
    from modules.models import ProgressRecord as _PR
    from modules.models import SimulationResult as _SR
    from modules.models import TaskProgress as _TP

    n_lessons, _ = _PR.objects.filter(user=learner, lesson__module=module).delete()
    _TP.objects.filter(user=learner, task__lesson__module=module).delete()
    QuizResult.objects.filter(user=learner, quiz__module=module).delete()
    _SR.objects.filter(user=learner, simulation__module=module).delete()
    g.refresh_profile(learner)
    return n_lessons


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
