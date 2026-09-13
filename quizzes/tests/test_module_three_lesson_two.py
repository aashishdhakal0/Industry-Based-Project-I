"""Module 3, Lesson 2 ("Read it like an analyst: spot, verify, report") — the
hands-on rebuild. Almost entirely phone-framed, distinct in character from
Modules 1 and 2's desktop consoles: a lock-screen notification stack (CLASSIFY),
two SMS threads side by side (SPOT), a raw email header block (NETMAP), a live
incoming call with a scrolling transcript (BRANCH), and a voicemail inbox
(MAILSORT). These tests check the new phone-shaped payloads are well-formed and
that the module reads as one continuous story (same trades business, same cast,
both lessons).
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

CAST = ("Wayne Castellano", "Bianca Okafor", "Rhonda Steel", "Liam Dorsett")
BUSINESS = "Sunbury Plumbing & Gas"


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner-m3l2@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=3)


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
        ("name-the-lever", "CLASSIFY"),
        ("two-texts", "SPOT"),
        ("forged-headers", "NETMAP"),
        ("the-clone-call", "BRANCH"),
        ("triage-voicemail", "MAILSORT"),
    ]
    actual = [(t.task_key, t.kind) for t in sorted(l2_tasks.values(), key=lambda t: t.order)]
    assert actual == expected_order


# --------------------------------------------------------------------------
# Payload well-formedness for each new phone-shaped artefact
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_classify_lockscreen_is_well_formed(l2_tasks):
    p = l2_tasks["name-the-lever"].payload
    assert p.get("phone") is True
    cats = {c["id"] for c in p["categories"]}
    assert cats == {"authority", "urgency", "fear", "curiosity", "greed"}
    events = p["events"]
    assert len(events) == 5
    for e in events:
        assert e["category"] in cats
        assert e.get("app") and e.get("from") and e.get("preview") and e.get("why")
    # Every lever is used exactly once: a clean 1:1 teaching mapping.
    assert {e["category"] for e in events} == cats


@pytest.mark.django_db
def test_spot_sms_threads_are_well_formed(l2_tasks):
    p = l2_tasks["two-texts"].payload
    assert p["variant"] == "sms"
    assert p["fake"] in ("left", "right")
    for side in ("left", "right"):
        thread = p[side]
        assert thread.get("bubbles") and isinstance(thread["bubbles"], list)
        assert thread.get("contact") or thread.get("number")
    # The fake side is the one without a saved contact name (a bare number),
    # which is itself part of the tell.
    fake = p[p["fake"]]
    real = p["left" if p["fake"] == "right" else "right"]
    assert not fake.get("contact"), "the trap should come from an unsaved number"
    assert real.get("contact"), "the genuine thread should come from a saved contact"
    assert p.get("why")


@pytest.mark.django_db
def test_netmap_header_inspection_is_well_formed(l2_tasks):
    p = l2_tasks["forged-headers"].payload
    assert p["frame"]["tab"]
    assert p.get("heading") and p.get("lede")
    nodes = p["nodes"]
    assert len(nodes) == 6
    weak = [n for n in nodes if n["weak"]]
    ok = [n for n in nodes if not n["weak"]]
    assert len(weak) == 3 and len(ok) == 3
    for n in nodes:
        assert n.get("label") and n.get("detail") and n.get("why")
    # The forged lines are the routing headers, not the display name.
    weak_labels = " ".join(n["label"] for n in weak)
    assert "Reply-To" in weak_labels and "Return-Path" in weak_labels and "Received" in weak_labels
    ok_labels = " ".join(n["label"] for n in ok)
    assert ok_labels.startswith("From:") or "From:" in ok_labels


@pytest.mark.django_db
def test_branch_call_is_well_formed(l2_tasks):
    task = l2_tasks["the-clone-call"]
    p = task.payload
    assert p["variant"] == "call"
    assert p.get("caller") and p.get("start") in p["nodes"]
    nodes = p["nodes"]
    seen, stack, outcomes, endings = set(), [p["start"]], set(), []
    while stack:
        nid = stack.pop()
        if nid in seen:
            continue
        seen.add(nid)
        node = nodes[nid]
        assert node.get("text")
        for c in node.get("choices", []):
            assert c.get("label") and c.get("feedback") and c["to"] in nodes
            outcomes.add(c["outcome"])
            stack.append(c["to"])
        if not node.get("choices"):
            endings.append(nid)
    assert set(nodes) == seen, "unreachable node in the clone-call branch"
    assert "good" in outcomes and "bad" in outcomes
    assert len(endings) >= 2


@pytest.mark.django_db
def test_mailsort_voicemail_is_well_formed(l2_tasks):
    p = l2_tasks["triage-voicemail"].payload
    assert p["variant"] == "voicemail"
    vms = p["voicemails"]
    assert len(vms) == 5
    phish = [v for v in vms if v["phish"]]
    genuine = [v for v in vms if not v["phish"]]
    assert len(phish) == 2 and len(genuine) == 3
    for v in vms:
        assert v.get("from") and v.get("time") and v.get("duration")
        assert v.get("transcript") and v.get("why")
    # The two scams are the module's two BEC flavours: a police-impersonation
    # vishing voicemail and an invoice/bank-change fraud voicemail, not the
    # same story told twice.
    scam_text = " ".join(v["transcript"] for v in phish)
    assert "warrant" in scam_text.lower() or "police" in scam_text.lower()
    assert "bank details" in scam_text.lower() or "bsb" in scam_text.lower()


# --------------------------------------------------------------------------
# Continuity: one story, same cast and business, across both lessons
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_establishes_one_consistent_story(seeded):
    l2 = seeded.lessons.get(lesson_number=2)
    # The business name itself carries a literal "&", which the sanitiser
    # stores as the HTML entity &amp; — unescape before comparing.
    intro = _html.unescape(l2.body_text)
    l2_blob = _html.unescape(
        " ".join((t.body or "") + _json.dumps(t.payload or {}) for t in l2.tasks.all())
    )
    assert BUSINESS in intro and BUSINESS in l2_blob
    for name in CAST:
        assert name in intro, f"{name} should be introduced in Lesson 2's intro"
    for first_name in (n.split()[0] for n in CAST):
        assert first_name in l2_blob, f"{first_name} should appear across Lesson 2's tasks"


# --------------------------------------------------------------------------
# Rendered page: real interactive DOM
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_page_renders_all_five_activity_kinds(seeded):
    student = User.objects.create_user(
        email="m3l2-learner@example.com", password="x" * 14, is_verified=True
    )
    # Module 3 is sequentially locked behind Modules 1 and 2 (a real 403,
    # exercised under test since DEBUG is forced off).
    for order in (1, 2):
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
        reverse("learn:lesson", args=[3, 2]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    for kind in ("CLASSIFY", "SPOT", "NETMAP", "BRANCH", "MAILSORT"):
        assert f'data-activity-kind="{kind}"' in html, f"{kind} activity missing from Lesson 2"
    assert "<img" not in html
