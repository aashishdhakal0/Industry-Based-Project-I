"""Training content: modules, their lessons and simulations, and progress."""

from django.conf import settings
from django.db import models


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
