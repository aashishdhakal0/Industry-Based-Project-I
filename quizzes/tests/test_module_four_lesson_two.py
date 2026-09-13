"""Module 4, Lesson 2 ("Put it to work: sharing safely, files, links, and
Wi-Fi") — the hands-on rebuild. Settings panels, toggles and modal overlays, a
register distinct from Modules 1-2's desktop consoles and Module 3's phone
apps: a real activity-log page (SORT), a browser's connection-details panel
(NETMAP), a floating Drive-style share dialog (HARDEN), an evil-twin Wi-Fi
picker to sequence a response to (SEQUENCE), and a live privacy-law incident
board (TABLETOP). These tests check the new artefact payloads are well-formed
and that the module reads as one continuous story (same firm, same cast, both
lessons).
"""

import html as _html
import json as _json

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client
from django.urls import reverse

from modules import gamification as g
from modules.models import Module
from quizzes.models import Quiz, QuizResult

User = get_user_model()

CAST = ("Farah Haddad", "Owen Tran", "Steph Corrigan")
BUSINESS = "Coburg Migration & Legal"


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner-m4l2@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=4)


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
        ("sealed-or-postcard", "SORT"),
        ("read-connection-panel", "NETMAP"),
        ("fix-share-settings", "HARDEN"),
        ("departure-gate", "SEQUENCE"),
        ("the-leaked-file", "TABLETOP"),
    ]
    actual = [(t.task_key, t.kind) for t in sorted(l2_tasks.values(), key=lambda t: t.order)]
    assert actual == expected_order


# --------------------------------------------------------------------------
# Payload well-formedness for each new artefact shape
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_sort_activity_log_is_well_formed(l2_tasks):
    p = l2_tasks["sealed-or-postcard"].payload
    assert p["frame"]["tab"] and p.get("heading")
    bucket_ids = {b["id"] for b in p["buckets"]}
    assert bucket_ids == {"enc", "open"}
    items = p["items"]
    assert len(items) == 6
    enc = [i for i in items if i["bucket"] == "enc"]
    open_ = [i for i in items if i["bucket"] == "open"]
    assert len(enc) == 3 and len(open_) == 3
    for i in items:
        assert i.get("text") and i.get("why")


@pytest.mark.django_db
def test_netmap_connection_panel_is_well_formed(l2_tasks):
    p = l2_tasks["read-connection-panel"].payload
    assert p["frame"]["tab"] and p.get("heading") and p.get("lede")
    nodes = p["nodes"]
    assert len(nodes) == 5
    weak = [n for n in nodes if n["weak"]]
    ok = [n for n in nodes if not n["weak"]]
    assert len(weak) == 2 and len(ok) == 3
    for n in nodes:
        assert n.get("label") and n.get("detail") and n.get("why")
    # The tell is the address and the unverified identity, not the encryption
    # or the certificate, which are both genuinely fine.
    weak_labels = " ".join(n["label"] for n in weak)
    assert "Address" in weak_labels and "identity" in weak_labels
    ok_labels = " ".join(n["label"] for n in ok)
    assert "Connection" in ok_labels and "Certificate" in ok_labels


@pytest.mark.django_db
def test_harden_sharemodal_is_well_formed(l2_tasks):
    task = l2_tasks["fix-share-settings"]
    p = task.payload
    assert p["variant"] == "sharemodal"
    assert p.get("heading") and p.get("file")
    steps = p["steps"]
    assert len(steps) == 4
    for step in steps:
        assert step.get("label") and step.get("value") and step.get("risk")
        correct = [o for o in step["options"] if o["correct"]]
        assert len(correct) == 1, f"{step['label']} must have exactly one correct fix"
        for opt in step["options"]:
            assert opt.get("text") and opt.get("why")
    # The four fields are the ones Lesson 1 actually taught: general access,
    # role (least access), expiry, and keeping the password on a separate
    # channel from the file.
    labels = {s["label"] for s in steps}
    assert labels == {"General access", "Role", "Link expiry", "Note to recipient"}


@pytest.mark.django_db
def test_sequence_departure_gate_is_well_formed(l2_tasks):
    task = l2_tasks["departure-gate"]
    assert task.diagram_key == "wifi-picker-evil-twin"
    p = task.payload
    steps = p["steps"]
    assert len(steps) == 5
    orders = sorted(s["order"] for s in steps)
    assert orders == [1, 2, 3, 4, 5]
    for step in steps:
        assert step.get("label") and step.get("detail")
    by_order = {s["order"]: s["label"] for s in steps}
    assert "wi-fi" in by_order[1].lower() or "near-identical" in by_order[1].lower()
    assert "lock" in by_order[4].lower()


@pytest.mark.django_db
def test_tabletop_leaked_file_is_well_formed(l2_tasks):
    p = l2_tasks["the-leaked-file"].payload
    assert p.get("scenario")
    board = p["board"]
    assert len(board) == 3
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
            for ind_id in (opt.get("board") or {}):
                assert ind_id in board_ids, f"unknown board indicator {ind_id}"
    # The climax names the actual legal duty from Lesson 1's sibling module,
    # not a vague "be careful" resolution.
    assert "privacy act" in _json.dumps(stages).lower() or "notifiable" in _json.dumps(stages).lower()


# --------------------------------------------------------------------------
# Continuity: one story, same cast and business, across both lessons
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_continues_the_same_story_as_lesson_one(seeded):
    l1 = seeded.lessons.get(lesson_number=1)
    l2 = seeded.lessons.get(lesson_number=2)
    l1_blob = _html.unescape((l1.body_text or ""))
    l2_intro = _html.unescape(l2.body_text)
    l2_blob = _html.unescape(
        " ".join((t.body or "") + _json.dumps(t.payload or {}) for t in l2.tasks.all())
    )
    assert BUSINESS in l2_intro and BUSINESS in l2_blob
    for name in CAST:
        assert name in l2_intro, f"{name} should be introduced in Lesson 2's intro"
    for first_name in (n.split()[0] for n in CAST):
        assert first_name in l2_blob, f"{first_name} should appear across Lesson 2's tasks"


# --------------------------------------------------------------------------
# Rendered page: real interactive DOM
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_page_renders_all_five_activity_kinds(seeded):
    student = User.objects.create_user(
        email="m4l2-learner@example.com", password="x" * 14, is_verified=True
    )
    # Module 4 is sequentially locked behind Modules 1-3 (a real 403, exercised
    # under test since DEBUG is forced off).
    for order in (1, 2, 3):
        m = Module.objects.get(order_index=order)
        for lesson in m.lessons.order_by("lesson_number"):
            g.complete_lesson(student, lesson)
        QuizResult.objects.create(
            user=student, quiz=Quiz.objects.get(module=m),
            attempt_number=1, score=100, passed=True,
        )
    g.refresh_profile(student)

    client = Client()
    client.force_login(student)
    html = client.get(
        reverse("learn:lesson", args=[4, 2]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    for kind in ("SORT", "NETMAP", "HARDEN", "SEQUENCE", "TABLETOP"):
        assert f'data-activity-kind="{kind}"' in html, f"{kind} activity missing from Lesson 2"
    assert "<img" not in html
