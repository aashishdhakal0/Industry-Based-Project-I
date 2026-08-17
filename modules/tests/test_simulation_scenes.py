"""Modules 1 and 2 ship a scene-based branching simulation.

The redesigned simulation is a visual, scene-by-scene story: each scene has a
backdrop, a narrative and choices; picking one reveals a consequence and advances
to the next scene, ending in a summary. This checks the seeded data is a
well-formed, fully solvable branching graph (every scene reachable, at least one
ending, each decision offering a sound and an unsound option), and that the page
renders with the scene data for cybaroo.js to drive.
"""

import json

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules.models import Module

User = get_user_model()


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="sim-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")


@pytest.mark.django_db
@pytest.mark.parametrize("order_index", [1, 2])
def test_module_has_a_wellformed_scene_simulation(seeded, order_index):
    module = Module.objects.get(order_index=order_index)
    data = module.simulation.decision_points
    assert data.get("kind") == "scenes", "Modules 1 and 2 use the scene simulation"
    assert data.get("intro")
    scenes = data["scenes"]
    start = data["start"]
    assert start in scenes

    # Walk the graph from the start: every scene must be reachable, every choice
    # must point at a real scene, and there must be at least one ending.
    seen, stack, endings, decisions = set(), [start], [], []
    while stack:
        sid = stack.pop()
        if sid in seen:
            continue
        seen.add(sid)
        scene = scenes[sid]
        assert scene.get("title") and scene.get("narrative"), f"{sid} needs title + narrative"
        assert scene.get("backdrop"), f"{sid} needs a backdrop"
        choices = scene.get("choices", [])
        if not choices:
            endings.append(sid)
            continue
        decisions.append(sid)
        outcomes = set()
        for ch in choices:
            assert ch.get("label") and ch.get("consequence"), f"{sid} choice needs label + consequence"
            assert ch["to"] in scenes, f"{sid} choice points at missing scene {ch['to']}"
            outcomes.add(ch["outcome"])
            stack.append(ch["to"])
        # A genuine decision offers a sound call and at least one costly one.
        assert "good" in outcomes, f"{sid} needs a sound (good) option"
        assert outcomes - {"good"}, f"{sid} needs at least one unsound option"

    assert set(scenes) == seen, f"unreachable scenes: {set(scenes) - seen}"
    assert len(decisions) == 2, "the simulation is exactly two (richer) decision scenes"
    assert endings, "the simulation needs an ending scene"


@pytest.mark.django_db
@pytest.mark.parametrize("order_index", [1, 2])
def test_simulation_page_renders_the_scene_data(seeded, order_index):
    student = User.objects.create_user(
        email=f"sim-learner-{order_index}@example.com", password="x" * 14, is_verified=True
    )
    from modules import gamification as g
    from quizzes.models import Quiz, QuizResult

    # Unlock module 2 by completing module 1 for the order_index==2 case.
    if order_index == 2:
        m1 = Module.objects.get(order_index=1)
        for lesson in m1.lessons.all():
            g.complete_lesson(student, lesson)
        QuizResult.objects.create(
            user=student, quiz=Quiz.objects.get(module=m1),
            attempt_number=1, score=100, passed=True,
        )
        g.refresh_profile(student)

    from django.test import Client
    client = Client()
    client.force_login(student)
    resp = client.get(reverse("learn:simulation", args=[order_index]), HTTP_HOST="127.0.0.1")
    assert resp.status_code == 200
    html = resp.content.decode()
    assert 'id="cy-sim"' in html and 'id="cy-sim-data"' in html
    # The scene JSON is present for cybaroo.js to read.
    assert '"kind": "scenes"' in html or '"kind":"scenes"' in html
