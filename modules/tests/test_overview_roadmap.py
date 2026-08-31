"""The module overview roadmap: lesson cards with task chips, a sim and quiz card.

Guards the two rendering bugs that were fixed here:
  - the "Start" CTA must render its visible text label (it was cyan-on-cyan,
    invisible, because the global `.cy-body a` rule overrode the button colour);
  - the roadmap must use its own `cy-mroad` namespace, not `cy-road` (the
    dashboard's horizontal progress track) whose styles were leaking in.
Plus the task-type chips carry an icon and a per-kind colour class.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

from modules.models import Module

User = get_user_model()


@pytest.fixture
def client_at_module_one(db):
    User.objects.create_user(
        email="road-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="road-learner@example.com", password="x" * 14, is_verified=True
    )
    client = Client()
    client.force_login(student)
    return client


@pytest.mark.django_db
def test_overview_uses_its_own_namespace_not_the_dashboard_track(client_at_module_one):
    html = client_at_module_one.get(
        reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    assert 'class="cy-mroad' in html
    # The clashing class names must be gone from this page.
    assert "cy-road__" not in html
    assert "cy-scene" not in html


@pytest.mark.django_db
def test_the_start_cta_renders_a_visible_text_label(client_at_module_one):
    html = client_at_module_one.get(
        reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    ctas = [
        re.sub(r"<[^>]+>", "", body).strip()
        for body in re.findall(r'<a class="cy-mroad__cta[^"]*"[^>]*>(.*?)</a>', html, re.S)
    ]
    # A fresh learner sees "Start" on the simulation card. The label must be a
    # real text node in the CTA (the bug was the text being invisible, not absent,
    # but an empty label would also fail here).
    assert any(text == "Start" for text in ctas), f"no visible Start CTA: {ctas}"
    assert all(text for text in ctas), "a CTA rendered with no text label"


@pytest.mark.django_db
def test_task_chips_carry_an_icon_and_a_per_kind_class(client_at_module_one):
    html = client_at_module_one.get(
        reverse("learn:module", args=[1]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    chips = re.findall(
        r'cy-mroad__chip cy-mroad__chip--(\w+)"><svg[^>]*><use href="#(i-[a-z-]+)"', html
    )
    assert chips, "task chips should render with a kind class and an icon"
    kinds = {k for k, _ in chips}
    # Module 1 now teaches then applies: L1 is CONCEPT x4 + CHECK, L2 is
    # CLASSIFY / BRANCH / SORT / CHECK / RESPOND.
    assert {"concept", "check", "classify", "respond"} <= kinds, f"chip kinds: {kinds}"
    # Distinct types map to distinct icons (not one repeated badge).
    by_kind = dict(chips)
    assert by_kind["concept"] == "i-book"
    assert by_kind["check"] == "i-check-circle"
    assert by_kind["respond"] == "i-branch"
