"""Module 1 is content-complete: interactive task lessons and a valid quiz bank.

These tests guard the *content contract* — that the seed produces genuine
interactive lessons (tasks that sum to a lesson's points, real scenarios, options
that are explained) and a quiz bank the engine and AFE can rely on.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from modules.gamification import POINTS_PER_LESSON
from modules.models import LessonTask, Module
from quizzes.models import Answer

User = get_user_model()

MIN_TASK_WORDS = 300  # genuine teaching content, now chunked across a lesson's tasks


def words_in(html):
    return len(re.sub(r"<[^>]+>", " ", html or "").split())


def task_content_words(task):
    """All the words a task teaches: its body plus the question, scenario and
    option explanations in its payload."""
    n = words_in(task.body)
    payload = task.payload or {}
    n += words_in(payload.get("question", "")) + words_in(payload.get("scenario", ""))
    for opt in payload.get("options", []):
        n += words_in(opt.get("text", "")) + words_in(opt.get("explanation", ""))
    return n


@pytest.fixture
def seeded(db):
    # The seeder needs a user to own the content.
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=1)


@pytest.mark.django_db
def test_module_one_lessons_are_interactive_task_sequences(seeded):
    lessons = list(seeded.lessons.order_by("lesson_number"))
    assert len(lessons) == 4
    for lesson in lessons:
        tasks = list(lesson.tasks.order_by("order"))
        assert len(tasks) >= 4, f"{lesson.title} has too few tasks"
        # Tasks subdivide the lesson's points and must sum to the lesson value,
        # or the XP bar won't match what's banked on completion.
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} XP != {POINTS_PER_LESSON}"
        # Genuine teaching content, now chunked across the tasks (bodies + the
        # questions, scenarios and explanations the tasks carry).
        words = sum(task_content_words(t) for t in tasks)
        assert words >= MIN_TASK_WORDS, f"{lesson.title} task content is too thin ({words} words)"


@pytest.mark.django_db
def test_module_one_has_hands_on_scenarios(seeded):
    scenarios = LessonTask.objects.filter(
        lesson__module=seeded, kind=LessonTask.Kind.SCENARIO
    )
    # The brief asks for at least one problem-solving scenario; we have several.
    assert scenarios.count() >= 1
    # The flagship "spot the risk" scenario lives in Lesson 2.
    assert scenarios.filter(lesson__lesson_number=2).exists()


@pytest.mark.django_db
def test_check_and_scenario_options_are_well_formed_and_explained(seeded):
    interactive = LessonTask.objects.filter(lesson__module=seeded).exclude(
        kind=LessonTask.Kind.CONCEPT
    )
    assert interactive.exists()
    for task in interactive:
        options = task.payload.get("options", [])
        assert len(options) == 4, f"{task.task_key} should have four options"
        assert sum(1 for o in options if o["correct"]) == 1, f"{task.task_key} needs exactly one correct option"
        for o in options:
            assert o["explanation"].strip(), f"{task.task_key} has an unexplained option"
        assert task.payload.get("question"), f"{task.task_key} has no question"


@pytest.mark.django_db
def test_module_one_covers_the_required_ground(seeded):
    # Search the real teaching surface: intros, task bodies, and payloads.
    parts = [l.body_text for l in seeded.lessons.all()]
    for t in LessonTask.objects.filter(lesson__module=seeded):
        parts.append(t.body)
        parts.append(str(t.payload))
    corpus = " ".join(parts).lower()
    assert "confidentiality" in corpus and "integrity" in corpus and "availability" in corpus
    assert "network" in corpus
    assert "phishing" in corpus
    assert "human error" in corpus


@pytest.mark.django_db
def test_module_one_quiz_has_a_bank_of_at_least_fifteen(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() >= 15


@pytest.mark.django_db
def test_every_question_is_well_formed_for_the_engine_and_the_afe(seeded):
    for q in seeded.quiz.questions.all():
        answers = list(q.answers.all())
        assert len(answers) == 4, f"{q} does not have exactly four options"
        assert sum(1 for a in answers if a.correct_answer) == 1, f"{q} needs exactly one correct option"
        # Every option must be explained — the AFE reads this back to the learner.
        for a in answers:
            assert a.explanation_text.strip(), f"{q} has an option with no explanation"


@pytest.mark.django_db
def test_every_question_traces_to_a_module_one_lesson(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.select_related("lesson_reference"):
        assert q.lesson_reference_id in lesson_ids, f"{q} references a lesson outside Module 1"


@pytest.mark.django_db
def test_the_seed_is_idempotent(seeded):
    """Re-running must update in place, not duplicate lessons, tasks, questions."""
    quiz = seeded.quiz

    def counts():
        return (
            seeded.lessons.count(),
            LessonTask.objects.filter(lesson__module=seeded).count(),
            quiz.questions.count(),
            Answer.objects.filter(question__quiz=quiz).count(),
        )

    before = counts()
    call_command("seed_learning_content")
    assert before == counts()
