"""The real student quiz page is an interactive, one-question-at-a-time paper.

Guards the redesign: the quiz ships each option with a `data-correct` flag and a
hidden explanation (so quiz.js can give immediate correct/incorrect feedback,
exactly like the in-lesson CHECK activities), a per-question difficulty tag, and a
feedback slot, WITHOUT pre-revealing the answers (no reveal classes in the served
HTML). The interactive behaviour itself (select -> reveal -> lock -> Next) is
proven by the jsc DOM harness in the session scratchpad. Server-side grading is
untouched and covered by test_services.py.

The dev-only review page keeps its own, separate behaviour: it deliberately shows
every answer and explanation at once, and is covered by test_quiz_review.py.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules import gamification as g
from modules.models import Module

User = get_user_model()


@pytest.fixture
def student_at_quiz(client, db):
    User.objects.create_user(
        email="quiz-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="quiz-taker@example.com", password="x" * 14, is_verified=True
    )
    # The suite runs with DEBUG=False, so the real lesson gate is live: finish
    # Module 1's lessons to open its quiz.
    m1 = Module.objects.get(order_index=1)
    for lesson in m1.lessons.all():
        g.complete_lesson(student, lesson)
    g.refresh_profile(student)
    client.force_login(student)
    return client


@pytest.mark.django_db
def test_quiz_serves_one_fieldset_per_question_with_interactive_markup(student_at_quiz):
    html = student_at_quiz.get(reverse("learn:quiz", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    # Ten questions, each its own stepper fieldset.
    assert html.count("data-quiz-q") == 10
    # Four options per question, each carrying a data-correct flag and a hidden
    # explanation the JS reveals after the learner commits.
    assert html.count("data-opt") == 40
    assert html.count("cy-quiz__opt-why") == 40
    # Exactly one correct option per question is flagged for the client.
    assert html.count('data-correct="1"') == 10
    # A per-question difficulty tag and a feedback slot.
    assert html.count("cy-quiz__diff") == 10
    assert html.count("data-quiz-feedback") == 10
    # The stepper script is versioned (cache-buster).
    assert "quiz.js?v=" in html


@pytest.mark.django_db
def test_quiz_does_not_pre_reveal_the_answers(student_at_quiz):
    html = student_at_quiz.get(reverse("learn:quiz", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    # Options are neutral on load: none of the reveal-state classes are present
    # in the server HTML (they are added only by quiz.js after a selection).
    assert "is-answered" not in html
    assert not re.search(r'class="[^"]*\bis-correct\b', html)
    assert not re.search(r'class="[^"]*\bis-wrong\b', html)


@pytest.mark.django_db
def test_quiz_difficulty_tag_is_a_single_flat_style_not_per_level(student_at_quiz):
    html = student_at_quiz.get(reverse("learn:quiz", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    # One flat tag class, no per-level colour variants.
    assert "cy-quiz__diff" in html
    for variant in ("cy-quiz__diff--easy", "cy-quiz__diff--medium", "cy-quiz__diff--hard"):
        assert variant not in html
