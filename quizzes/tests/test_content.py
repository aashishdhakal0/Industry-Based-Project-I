"""Module 1 is content-complete: real lessons and a valid, seeded quiz bank.

These tests guard the *content contract* — that the seed produces genuine lessons
(not placeholders) and a bank the quiz engine and AFE can rely on: four options
per question, exactly one correct, every option explained, and every question
traceable to a Module 1 lesson.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from modules.models import Module
from quizzes.models import Answer

User = get_user_model()

MIN_WORDS = 700  # genuine lessons; the target is ~800, this is the floor with margin


def words_in(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


@pytest.fixture
def seeded(db):
    # The seeder needs a user to own the content.
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=1)


@pytest.mark.django_db
def test_module_one_has_four_real_substantial_lessons(seeded):
    lessons = list(seeded.lessons.order_by("lesson_number"))
    assert len(lessons) == 4
    for lesson in lessons:
        assert "Placeholder lesson" not in lesson.body_text, f"{lesson.title} is still a placeholder"
        assert words_in(lesson.body_text) >= MIN_WORDS, f"{lesson.title} is too short"


@pytest.mark.django_db
def test_module_one_covers_the_required_ground(seeded):
    corpus = " ".join(l.body_text for l in seeded.lessons.all()).lower()
    # The brief's required coverage, checked plainly.
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
    """Re-running must update in place, not duplicate lessons, questions or options."""
    quiz = seeded.quiz
    before = (
        seeded.lessons.count(),
        quiz.questions.count(),
        Answer.objects.filter(question__quiz=quiz).count(),
    )
    call_command("seed_learning_content")
    after = (
        seeded.lessons.count(),
        quiz.questions.count(),
        Answer.objects.filter(question__quiz=quiz).count(),
    )
    assert before == after
