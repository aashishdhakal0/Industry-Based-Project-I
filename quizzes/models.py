"""Quiz engine models, and the data the Adaptive Feedback Engine reads."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from modules.models import Lesson, Module


class Quiz(models.Model):
    """The quiz for a module. One per module."""

    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name="quiz")
    time_limit_minutes = models.PositiveIntegerField(default=30)
    pass_mark = models.PositiveIntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage required to pass.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "quizzes"
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"Quiz — {self.module.title}"


class Question(models.Model):
    """A quiz question. Ten are drawn at random per attempt from the bank."""

    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    difficulty = models.CharField(
        max_length=20, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    ordering = models.PositiveIntegerField(default=0)

    # Required by the Adaptive Feedback Engine: it groups a student's mistakes by
    # the lesson that teaches the topic, and uses that lesson's reading time to
    # estimate revision effort. Absent from the spec's field list — added
    # deliberately, since the AFE cannot work without it.
    lesson_reference = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="questions",
        help_text="The lesson that teaches this question's topic.",
    )
    admin_edited = models.BooleanField(
        default=False,
        help_text="An admin has edited this question (or its answers) in the "
        "console. The seed leaves such rows alone (unless run with --force).",
    )

    class Meta:
        db_table = "questions"
        ordering = ["ordering"]

    def __str__(self):
        return self.question_text[:80]


class Answer(models.Model):
    """One of exactly four options (A-D) for a question.

    `explanation_text` is the fuel for the Adaptive Feedback Engine — the whole
    product rests on the quality of this field.
    """

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    option_text = models.CharField(max_length=500)
    correct_answer = models.BooleanField(default=False)
    explanation_text = models.TextField(
        help_text="Why this option is right or wrong. Shown to the learner when "
        "they choose incorrectly."
    )

    class Meta:
        db_table = "answers"

    def __str__(self):
        mark = "✓" if self.correct_answer else "✗"
        return f"{mark} {self.option_text[:60]}"


class QuizResult(models.Model):
    """One row per quiz attempt."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage.",
    )
    passed = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quiz_results"
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "quiz", "attempt_number"],
                name="unique_attempt_number_per_user_quiz",
            )
        ]

    def __str__(self):
        outcome = "passed" if self.passed else "failed"
        return f"{self.user.email} {outcome} {self.quiz} ({self.score}%)"


class WrongAnswer(models.Model):
    """One row per incorrect response. The Adaptive Feedback Engine's input."""

    quiz_result = models.ForeignKey(
        QuizResult, on_delete=models.CASCADE, related_name="wrong_answers"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="wrong_answers"
    )
    student_answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="chosen_wrongly_in",
        help_text="The option the student picked.",
    )
    correct_answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="missed_in",
        help_text="The option they should have picked.",
    )

    class Meta:
        db_table = "wrong_answers"
        constraints = [
            models.UniqueConstraint(
                fields=["quiz_result", "question"],
                name="unique_wrong_answer_per_question_per_attempt",
            )
        ]

    def __str__(self):
        return f"Wrong: {self.question}"
