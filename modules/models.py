"""Training content: modules, their lessons and simulations, and progress."""

import nh3
from django.conf import settings
from django.db import models

# The allow-list for lesson HTML. Lessons render UNESCAPED, so this is the only
# thing standing between an author (or a compromised CMS session) and stored
# XSS in every student's browser — a CLAUDE.md "never". Anything not named here
# is stripped: no <script>, no <iframe>, no event-handler attributes, no
# javascript: URLs (nh3 drops those by default).
LESSON_ALLOWED_TAGS = {
    "h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "em", "u",
    "a", "img", "blockquote", "code", "pre", "hr", "br", "table",
    "thead", "tbody", "tr", "th", "td", "figure", "figcaption", "span", "div",
}
LESSON_ALLOWED_ATTRIBUTES = {
    # No "rel" here — link_rel below manages it (nh3 forbids doing both), adding
    # rel="noopener noreferrer" to every link so a lesson can't reach back into
    # our tab via window.opener.
    "a": {"href", "title"},
    "img": {"src", "alt", "title", "width", "height"},
    "span": {"class"},
    "div": {"class"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}


def sanitise_lesson_html(html):
    """Strip anything not on the lesson allow-list. Safe to call twice."""
    return nh3.clean(
        html or "",
        tags=LESSON_ALLOWED_TAGS,
        attributes=LESSON_ALLOWED_ATTRIBUTES,
        link_rel="noopener noreferrer",
    )


class Module(models.Model):
    """One of the six training modules.

    `order_index` drives the sequential lock: a student may only open module N
    once module N-1 is complete.
    """

    class Difficulty(models.TextChoices):
        BEGINNER = "BEGINNER", "Beginner"
        INTERMEDIATE = "INTERMEDIATE", "Intermediate"
        ADVANCED = "ADVANCED", "Advanced"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER
    )
    duration_minutes = models.PositiveIntegerField(
        default=0, help_text="Estimated time to complete the whole module."
    )
    order_index = models.PositiveIntegerField(
        unique=True, help_text="Position in the sequential unlock order (1-6)."
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Unpublishing is our soft delete — never hard-delete a module, "
        "it would orphan historical quiz results.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="modules_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "modules"
        ordering = ["order_index"]

    def __str__(self):
        return f"{self.order_index}. {self.title}"


class Lesson(models.Model):
    """A single lesson within a module. Four per module."""

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons"
    )
    lesson_number = models.PositiveIntegerField(help_text="Order within the module.")
    title = models.CharField(max_length=255)
    body_text = models.TextField(
        help_text="TinyMCE HTML. MUST be sanitised on save — it renders unescaped."
    )
    reading_time_minutes = models.PositiveIntegerField(
        default=0, help_text="Used by the adaptive feedback engine to estimate revision time."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "lessons"
        ordering = ["module__order_index", "lesson_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["module", "lesson_number"], name="unique_lesson_number_per_module"
            )
        ]

    def save(self, *args, **kwargs):
        # Sanitise on the way IN, so the database only ever holds clean HTML and
        # every read path — student viewer, admin preview, exports — is safe by
        # construction. Sanitising on render instead would mean remembering to
        # do it at every call site, and the first one forgotten is the hole.
        self.body_text = sanitise_lesson_html(self.body_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.title} — L{self.lesson_number}: {self.title}"


class Simulation(models.Model):
    """The interactive branching scenario for a module. One per module."""

    module = models.OneToOneField(
        Module, on_delete=models.CASCADE, related_name="simulation"
    )
    scenario_text = models.TextField(help_text="The opening scenario shown to the learner.")
    decision_points = models.JSONField(
        default=dict, help_text="Branching decision tree."
    )
    outcome_text = models.JSONField(
        default=dict,
        help_text="Outcomes keyed by decision path. JSON, not text: the spec "
        "describes one field holding 'each possible outcome', which a single "
        "text field cannot represent.",
    )

    class Meta:
        db_table = "simulations"

    def __str__(self):
        return f"Simulation for {self.module.title}"


class ProgressRecord(models.Model):
    """One row per lesson a student completes.

    Module completion % is derived by counting these against the module's lesson
    count — it is never stored.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress_records",
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress_records"
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "progress_records"
        constraints = [
            # A lesson counts once; re-reading must not inflate points.
            models.UniqueConstraint(
                fields=["user", "lesson"], name="unique_progress_per_user_lesson"
            )
        ]

    def __str__(self):
        return f"{self.user.email} completed {self.lesson}"


class SimulationResult(models.Model):
    """One row per time a student finishes a module's interactive simulation.

    New in Sprint 2. There was nowhere to record a simulation outcome —
    ProgressRecord is tied to a Lesson — so this is the one schema addition the
    student loop genuinely needs. Deliberately does NOT gate the sequential
    unlock (that stays lesson-based, per the spec); it records engagement and
    drives a badge. See the Sprint 2 plan.

    `path` stores the decisions the student made (which emails they judged, and
    how), so the simulation can show a personalised recap and so we can tell a
    perfect run from a scraped-through one later.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="simulation_results",
    )
    simulation = models.ForeignKey(
        Simulation, on_delete=models.CASCADE, related_name="results"
    )
    score = models.PositiveIntegerField(
        default=0, help_text="Correct decisions, out of the scenario's total."
    )
    total = models.PositiveIntegerField(
        default=0, help_text="Decisions available in the scenario."
    )
    path = models.JSONField(
        default=list, blank=True, help_text="The decisions the student made."
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "simulation_results"
        ordering = ["-completed_at"]
        constraints = [
            # One result per student per simulation: re-running overwrites via
            # update_or_create rather than piling up rows and re-awarding.
            models.UniqueConstraint(
                fields=["user", "simulation"], name="unique_simulation_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user.email} — {self.simulation} ({self.score}/{self.total})"


class LessonTask(models.Model):
    """One interactive step inside a lesson — the TryHackMe-style unit.

    A lesson is taught as an ordered sequence of these: a short concept, an
    inline check-question, or a real-world scenario. Authored in code and seeded
    into rows (the same author-then-seed pattern as the quiz bank), so the lesson
    view and progress can be generic and DB-driven.

    `points` are a display subdivision of the lesson's fixed value: a lesson's
    tasks sum to POINTS_PER_LESSON, and completing the last task banks that whole
    value through the normal ProgressRecord path — the points economy is
    unchanged, tasks just fill an XP bar on the way there.
    """

    class Kind(models.TextChoices):
        CONCEPT = "CONCEPT", "Concept"          # a short teaching intro
        CHECK = "CHECK", "Check question"        # legacy simple MCQ
        SCENARIO = "SCENARIO", "Scenario"        # legacy MCQ scenario
        # Interactive "do it" activities — config lives in `payload`.
        SORT = "SORT", "Sort into buckets"
        INBOX = "INBOX", "Inspect an inbox"
        SPOT = "SPOT", "Spot the fake"
        PASSWORD = "PASSWORD", "Password builder"
        BRANCH = "BRANCH", "Branching scenario"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="tasks"
    )
    order = models.PositiveIntegerField(default=0)
    task_key = models.CharField(
        max_length=80, help_text="Stable id within the lesson (for progress rows)."
    )
    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.CONCEPT
    )
    points = models.PositiveIntegerField(default=2)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True, help_text="Teaching HTML (sanitised on save).")
    diagram_key = models.CharField(
        max_length=40, blank=True, help_text="Names a CSS/SVG diagram partial."
    )
    payload = models.JSONField(
        default=dict,
        blank=True,
        help_text="For check/scenario tasks: scenario, question and options "
        "[{text, correct, explanation}].",
    )

    class Meta:
        db_table = "lesson_tasks"
        ordering = ["lesson__module__order_index", "lesson__lesson_number", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["lesson", "task_key"], name="unique_task_key_per_lesson"
            )
        ]

    def save(self, *args, **kwargs):
        # Developer-authored content, but sanitised anyway — defence in depth,
        # and it never strips the allow-listed tags we actually use.
        self.body = sanitise_lesson_html(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lesson} · task {self.order}: {self.task_key}"


class TaskProgress(models.Model):
    """One row per task a student completes — the truth behind the XP bar.

    A lesson counts as complete (and banks its points via ProgressRecord) once a
    student has a row for every one of its tasks. Persisting per task means a
    half-finished lesson resumes exactly where it was left.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_progress",
    )
    task = models.ForeignKey(
        LessonTask, on_delete=models.CASCADE, related_name="progress"
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_progress"
        ordering = ["-completed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "task"], name="unique_task_progress_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user.email} did {self.task}"
