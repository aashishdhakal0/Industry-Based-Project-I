"""Cross-module extras added in the Module 3/4 rebuild: the per-module tagline
(motto) shown on the overview, and the Module 1 hero illustration."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

from modules import gamification as g
from modules.models import LessonTask, Module

User = get_user_model()


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="extras-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")


@pytest.mark.django_db
def test_every_module_has_a_tagline_seeded(seeded):
    for m in Module.objects.all():
        assert m.tagline.strip(), f"module {m.order_index} has no tagline"


@pytest.mark.django_db
def test_module_one_overview_renders_its_tagline(seeded):
    student = User.objects.create_user(
        email="tag-learner@example.com", password="x" * 14, is_verified=True
    )
    client = Client()
    client.force_login(student)
    html = client.get(reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1").content.decode()
    assert "cy-module__tagline" in html
    assert Module.objects.get(order_index=1).tagline in html


@pytest.mark.django_db
def test_module_one_lesson_one_has_the_hero_illustration(seeded):
    # Lesson 1 opens on the net-scene data-flow hero (the teaching intro panel);
    # the router-admin visual now teaches "where the weak points are" a few panels
    # on, so both figures still appear on Lesson 1.
    intro = LessonTask.objects.get(lesson__module__order_index=1, task_key="net-basics")
    assert intro.payload.get("hero") == "net-scene"
    weak = LessonTask.objects.get(lesson__module__order_index=1, task_key="weak-points")
    assert weak.diagram_key == "router-admin"


@pytest.mark.django_db
def test_module_one_lesson_page_renders_the_hero_and_the_router_visual(seeded):
    student = User.objects.create_user(
        email="hero-learner@example.com", password="x" * 14, is_verified=True
    )
    client = Client()
    client.force_login(student)
    html = client.get(reverse("learn:lesson", args=[1, 1]), HTTP_HOST="127.0.0.1").content.decode()
    # The hero scene (its own class) and the existing router-admin picture-question
    # both appear on Lesson 1.
    assert "cy-scene2" in html
    assert "YOUR NETWORK" in html
    assert "cy-radmin" in html  # router-admin picture-question still present
