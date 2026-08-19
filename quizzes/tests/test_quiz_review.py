"""The DEBUG-only quiz-review page: a developer content-review tool.

It lists every question in a module's quiz with the correct answer and all
explanations, but only exists when DEBUG is on. It must never appear in
production, and it must not weaken the real quiz gate for students.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, override_settings
from django.urls import reverse

from modules.models import Module

User = get_user_model()


@pytest.fixture
def learner(db):
    User.objects.create_user(
        email="qr-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="qr-learner@example.com", password="x" * 14, is_verified=True
    )
    client = Client()
    client.force_login(student)
    return client, student


@override_settings(DEBUG=True)
@pytest.mark.django_db
def test_review_lists_every_question_with_answers_when_debug(learner):
    client, _ = learner
    module = Module.objects.get(order_index=1)
    resp = client.get(reverse("learn:quiz_review", args=[1]), HTTP_HOST="127.0.0.1")
    assert resp.status_code == 200
    html = resp.content.decode()
    total = module.quiz.questions.count()
    assert total == 10  # exactly ten questions per module now
    # One review card per question, one correct-answer mark per question.
    assert html.count("cy-qr__card") == total
    assert html.count("is-correct") == total
    # Grouped by the two lessons.
    assert html.count("cy-qr__lesson") == 2
    # No leaked template tokens.
    for token in ("{{", "{%", "{#"):
        assert token not in html


@override_settings(DEBUG=False)
@pytest.mark.django_db
def test_review_is_404_in_production(learner):
    client, _ = learner
    resp = client.get(reverse("learn:quiz_review", args=[1]), HTTP_HOST="127.0.0.1")
    assert resp.status_code == 404


@override_settings(DEBUG=True)
@pytest.mark.django_db
def test_overview_shows_the_dev_review_link_only_in_debug(learner):
    client, _ = learner
    html = client.get(reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    assert "cy-devlink" in html
    assert reverse("learn:quiz_review", args=[1]) in html


@override_settings(DEBUG=False)
@pytest.mark.django_db
def test_overview_hides_the_dev_review_link_in_production(learner):
    client, _ = learner
    html = client.get(reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    assert "cy-devlink" not in html
