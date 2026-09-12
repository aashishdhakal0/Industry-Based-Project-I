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
    assert "cy-mhead__tagline" in html
    assert Module.objects.get(order_index=1).tagline in html


@pytest.mark.django_db
def test_module_one_lesson_one_uses_technical_diagrams(seeded):
    # Lesson 1 is theory-only and its teaching panels use professional TECHNICAL
    # DIAGRAMS (own-origin inline-SVG partials), no animation. The router photo is
    # kept only as a supporting aid on the weak-points panel, beside its diagram.
    intro = LessonTask.objects.get(lesson__module__order_index=1, task_key="net-basics")
    assert intro.diagram_key == "net-topology"
    assert not (intro.image or {}).get("src") and not intro.payload.get("hero")
    # The weak-points panel now uses a device-framed router settings screen, and
    # the stock router photo has been removed entirely.
    weak = LessonTask.objects.get(lesson__module__order_index=1, task_key="weak-points")
    assert weak.diagram_key == "router-admin"
    assert not (weak.image or {}).get("src")


@pytest.mark.django_db
def test_module_one_lesson_page_renders_diagrams_and_no_animation(seeded):
    student = User.objects.create_user(
        email="hero-learner@example.com", password="x" * 14, is_verified=True
    )
    client = Client()
    client.force_login(student)
    html = client.get(reverse("learn:lesson", args=[1, 1]), HTTP_HOST="127.0.0.1").content.decode()
    # Teaching diagrams render as own-origin inline SVG; the weak-points and check
    # panels render device-framed recreations (router screen, browser sign-in);
    # no stock photos; no animation on this teaching lesson.
    assert "cy-td__svg" in html and "<svg" in html
    assert "cy-radmin__form" in html   # device-framed router settings screen
    assert "cy-signin" in html         # device-framed lookalike browser sign-in
    assert "m1-router.webp" not in html and "m1-network.webp" not in html   # no stock photos
    assert "cy-scene2" not in html
