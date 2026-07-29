"""Shared fixtures for the quiz-engine tests: a real module with a question bank.

The bank is built deterministically — option index 0 is always the correct one —
so tests can construct a paper of known correctness without guessing.
"""

import pytest
from django.contrib.auth import get_user_model

from modules.models import Lesson, Module
from quizzes.models import Answer, Question, Quiz

User = get_user_model()

BANK_SIZE = 12


@pytest.fixture
def student(db):
    return User.objects.create_user(
        email="quizzer@example.com", password="x" * 14, is_verified=True
    )


@pytest.fixture
def author(db):
    return User.objects.create_user(
        email="quizauthor@example.com", password="x" * 14, role=User.Role.ADMINISTRATOR
    )


def _make_module(author, index, *, lessons=4):
    module = Module.objects.create(
        title=f"Module {index}",
        description="…",
        order_index=index,
        is_published=True,
        created_by=author,
    )
    for n in range(1, lessons + 1):
        Lesson.objects.create(
            module=module,
            lesson_number=n,
            title=f"Lesson {n}",
            body_text="<p>Placeholder.</p>",
            reading_time_minutes=5,
        )
    return module


@pytest.fixture
def module(author):
    return _make_module(author, 1)


@pytest.fixture
def make_module(author):
    def _factory(index, **kwargs):
        return _make_module(author, index, **kwargs)

    return _factory


def _build_bank(quiz, size=BANK_SIZE):
    lessons = list(quiz.module.lessons.order_by("lesson_number"))
    for i in range(1, size + 1):
        question = Question.objects.create(
            quiz=quiz,
            question_text=f"Question {i}?",
            ordering=i,
            lesson_reference=lessons[(i - 1) % len(lessons)],
        )
        for j in range(4):
            Answer.objects.create(
                question=question,
                option_text=f"Q{i} option {j}",
                correct_answer=(j == 0),  # option 0 is always correct
                explanation_text=(
                    f"Option {j} is correct." if j == 0 else f"Option {j} is a trap."
                ),
            )


@pytest.fixture
def quiz(module):
    quiz = Quiz.objects.create(module=module, pass_mark=70)
    _build_bank(quiz)
    return quiz


def responses_for(questions, *, correct):
    """Build a {question_id: answer_id} map answering the first `correct`
    questions correctly and the rest with a wrong option (index 1)."""
    out = {}
    for n, q in enumerate(questions):
        options = sorted(q.answers.all(), key=lambda a: a.id)
        pick = options[0] if n < correct else options[1]
        out[q.id] = pick.id
    return out
