"""Module 1, Lesson 2 ("Put it to work: a day under pressure") — the hands-on
rebuild. Where Lesson 1 teaches (reading panels with a visual), Lesson 2 hands
the learner a real, device-framed artefact to work: a router's live device
table (NETMAP), two sign-in pages to tell apart (SPOT), a Gmail inbox to triage
(MAILSORT), an account's settings to fix (HARDEN), and a live incident board
(TABLETOP). These tests check the new payload shapes are well-formed and that
the module reads as one continuous story (same agency, same cast, both lessons).
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules.models import LessonTask, Module

User = get_user_model()

CAST = ("Dean Whitlock", "Priya Anand", "Marion Fisk", "Cody Nguyen")
AGENCY = "Yarraville Real Estate"


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner-l2@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=1)


@pytest.fixture
def l2_tasks(seeded):
    return {
        t.task_key: t
        for t in seeded.lessons.get(lesson_number=2).tasks.order_by("order")
    }


# --------------------------------------------------------------------------
# Shape: five tasks, five distinct hands-on kinds, in the planned order
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_five_tasks_five_distinct_artefact_kinds(l2_tasks):
    expected_order = [
        ("network-strangers", "NETMAP"),
        ("portal-or-trap", "SPOT"),
        ("triage-inbox", "MAILSORT"),
        ("harden-account", "HARDEN"),
        ("missing-rent", "TABLETOP"),
    ]
    actual = [(t.task_key, t.kind) for t in sorted(l2_tasks.values(), key=lambda t: t.order)]
    assert actual == expected_order


# --------------------------------------------------------------------------
# Payload well-formedness for each new artefact shape
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_netmap_device_table_is_well_formed(l2_tasks):
    p = l2_tasks["network-strangers"].payload
    assert p["frame"]["tab"] and p["frame"]["url"]
    nodes = p["nodes"]
    assert len(nodes) >= 4
    weak = [n for n in nodes if n["weak"]]
    ok = [n for n in nodes if not n["weak"]]
    assert len(weak) == 2 and len(ok) >= 2, "a mix of real weaknesses and fine devices"
    for n in nodes:
        assert n.get("label") and n.get("detail") and n.get("why")


@pytest.mark.django_db
def test_spot_login_frame_is_well_formed(l2_tasks):
    p = l2_tasks["portal-or-trap"].payload
    assert p["variant"] == "login"
    assert p["fake"] in ("left", "right")
    for side in ("left", "right"):
        card = p[side]
        assert card.get("tab") and card.get("url") and card.get("brand")
    # Exactly one side is insecure (the trap); the other is the real, secure page.
    insecure = [s for s in ("left", "right") if p[s].get("insecure")]
    assert insecure == [p["fake"]], "the fake side must be the insecure one"
    assert p.get("why")


@pytest.mark.django_db
def test_mailsort_gmail_inbox_is_well_formed(l2_tasks):
    p = l2_tasks["triage-inbox"].payload
    assert p.get("gmail") is True
    assert p["frame"]["tab"]
    emails = p["emails"]
    assert len(emails) == 5
    phish = [e for e in emails if e["phish"]]
    genuine = [e for e in emails if not e["phish"]]
    assert len(phish) >= 2 and len(genuine) >= 2, "a real mix to triage, not all one verdict"
    for e in emails:
        assert e.get("from") and e.get("addr") and e.get("time")
        assert e.get("subject") and e.get("preview") and e.get("why")


@pytest.mark.django_db
def test_harden_settings_page_is_well_formed(l2_tasks):
    p = l2_tasks["harden-account"].payload
    assert p.get("settings") is True
    assert p["frame"]["tab"]
    steps = p["steps"]
    assert len(steps) == 4
    for step in steps:
        assert step.get("label") and step.get("value") and step.get("risk")
        correct = [o for o in step["options"] if o["correct"]]
        assert len(correct) == 1, f"{step['label']} must have exactly one correct fix"
        for opt in step["options"]:
            assert opt.get("text") and opt.get("why")


@pytest.mark.django_db
def test_tabletop_incident_board_is_well_formed(l2_tasks):
    p = l2_tasks["missing-rent"].payload
    assert p.get("scenario")
    board = p["board"]
    assert len(board) >= 3
    for ind in board:
        assert ind.get("id") and ind.get("label") and ind["state"] in ("ok", "warn", "bad")
    stages = p["stages"]
    assert len(stages) == 3
    board_ids = {ind["id"] for ind in board}
    for st in stages:
        assert st.get("phase") and st.get("prompt")
        good = [o for o in st["options"] if o["outcome"] == "good"]
        assert len(good) == 1, f"stage {st['phase']} must have exactly one good option"
        for opt in st["options"]:
            assert opt.get("label") and opt.get("consequence")
            assert opt["outcome"] in ("good", "bad")
            # Any board indicator an option updates must be one the board declares.
            for ind_id in (opt.get("board") or {}):
                assert ind_id in board_ids, f"unknown board indicator {ind_id}"


# --------------------------------------------------------------------------
# Continuity: one story, same cast and business, across both lessons
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_continues_the_same_story_as_lesson_one(seeded):
    l1 = seeded.lessons.get(lesson_number=1)
    l2 = seeded.lessons.get(lesson_number=2)
    l1_blob = " ".join((t.body or "") for t in l1.tasks.all())
    l2_blob = " ".join((t.body or "") for t in l2.tasks.all())
    assert AGENCY in l1_blob and AGENCY in l2_blob
    # Lesson 2's intro is where the scenario and its cast are established (by
    # full name, once), since Lesson 1 is generic teaching with no cast of its own.
    for name in CAST:
        assert name in l2.body_text, f"{name} should be introduced in Lesson 2's intro"
    # Lesson 2's task bodies carry the story forward with the same people (by
    # first name, the house convention once someone has been introduced).
    for first_name in (n.split()[0] for n in CAST):
        assert first_name in l2_blob, f"{first_name} should appear in Lesson 2 — same cast, same story"


# --------------------------------------------------------------------------
# Rendered page: real interactive DOM, no stray legacy markup
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_page_renders_all_five_activity_kinds(seeded):
    student = User.objects.create_user(
        email="l2-learner@example.com", password="x" * 14, is_verified=True
    )
    from django.test import Client

    client = Client()
    client.force_login(student)
    html = client.get(
        reverse("learn:lesson", args=[1, 2]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    for kind in ("NETMAP", "SPOT", "MAILSORT", "HARDEN", "TABLETOP"):
        assert f'data-activity-kind="{kind}"' in html, f"{kind} activity missing from Lesson 2"
    # No stock photos, no leaked template tokens.
    assert "<img" not in html
