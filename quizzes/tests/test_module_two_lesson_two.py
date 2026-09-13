"""Module 2, Lesson 2 ("Put it to work: name it, triage it, react to it") — the
hands-on rebuild. Where Lesson 1 teaches, Lesson 2 hands the learner a real,
device-framed artefact to work: a Windows Security protection history (SORT), a
real Gmail inbox (MAILSORT), a ransom-lock screen and an ordering drill
(SEQUENCE), a real incident register (CLASSIFY), and a live ransomware incident
(BRANCH). These tests check the new payload shapes are well-formed and that the
module reads as one continuous story (same shop, same cast, both lessons).
"""

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

CAST = ("Rick Halloran", "Tanya Pillai", "Dolores Fenn", "Josh Tran")
SHOP = "Ballarat Auto Spares"


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner-m2l2@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=2)


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
        ("name-the-threat", "SORT"),
        ("triage-counter-inbox", "MAILSORT"),
        ("order-the-response", "SEQUENCE"),
        ("assess-the-breach", "CLASSIFY"),
        ("the-ransom-note", "BRANCH"),
    ]
    actual = [(t.task_key, t.kind) for t in sorted(l2_tasks.values(), key=lambda t: t.order)]
    assert actual == expected_order


# --------------------------------------------------------------------------
# Payload well-formedness for each new artefact shape
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_sort_protection_history_is_well_formed(l2_tasks):
    p = l2_tasks["name-the-threat"].payload
    assert p["frame"]["tab"] and p["frame"]["url"]
    bucket_ids = {b["id"] for b in p["buckets"]}
    assert bucket_ids == {"virus", "worm", "trojan", "spyware", "ransomware"}
    assert len(p["items"]) == 6
    for item in p["items"]:
        assert item["bucket"] in bucket_ids and item.get("text") and item.get("why")
    # Every malware family is represented at least once.
    assert {i["bucket"] for i in p["items"]} == bucket_ids


@pytest.mark.django_db
def test_mailsort_gmail_inbox_is_well_formed(l2_tasks):
    p = l2_tasks["triage-counter-inbox"].payload
    assert p.get("gmail") is True
    assert p["frame"]["tab"]
    emails = p["emails"]
    assert len(emails) == 5
    phish = [e for e in emails if e["phish"]]
    genuine = [e for e in emails if not e["phish"]]
    assert len(phish) >= 2 and len(genuine) >= 2
    for e in emails:
        assert e.get("from") and e.get("addr") and e.get("time")
        assert e.get("subject") and e.get("preview") and e.get("why")


@pytest.mark.django_db
def test_sequence_ransomware_response_is_well_formed(l2_tasks):
    task = l2_tasks["order-the-response"]
    assert task.diagram_key == "ransom-lock-full"
    p = task.payload
    steps = p["steps"]
    assert len(steps) == 5
    orders = sorted(s["order"] for s in steps)
    assert orders == [1, 2, 3, 4, 5]
    for step in steps:
        assert step.get("label") and step.get("detail")
    # The order is a genuine cause-and-effect chain: disconnect precedes
    # confirming the backup, which precedes wiping and restoring.
    by_order = {s["order"]: s["label"] for s in steps}
    assert "disconnect" in by_order[1].lower()
    assert "restore" in by_order[4].lower()


@pytest.mark.django_db
def test_classify_incident_register_is_well_formed(l2_tasks):
    p = l2_tasks["assess-the-breach"].payload
    assert p["frame"]["tab"]
    cats = {c["id"] for c in p["categories"]}
    assert cats == {"notify", "assess", "not"}
    events = p["events"]
    assert len(events) == 6
    for e in events:
        assert e["category"] in cats and e.get("text") and e.get("why")
    assert {e["category"] for e in events} == cats, "every category must be used"


@pytest.mark.django_db
def test_branch_ransom_note_is_well_formed(l2_tasks):
    task = l2_tasks["the-ransom-note"]
    assert task.payload.get("hero") == "infection-spread"  # the "watch it happen" opener, kept from before
    p = task.payload
    assert p.get("prompt") and p["start"] in p["nodes"]
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
    assert set(nodes) == seen, "unreachable node in the ransom-note branch"
    assert "good" in outcomes and "bad" in outcomes
    assert len(endings) >= 2


# --------------------------------------------------------------------------
# Continuity: one story, same cast and business, across both lessons
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_establishes_one_consistent_story(seeded):
    """Module 2's Lesson 1 is pure concept teaching with no scenario of its own
    (unlike Module 1). Lesson 2 is where the shop and its cast are established,
    by full name in the intro, and carried through every task by first name."""
    l2 = seeded.lessons.get(lesson_number=2)
    l2_blob = " ".join(
        (t.body or "") + _json.dumps(t.payload or {}) for t in l2.tasks.all()
    )
    assert SHOP in l2.body_text and SHOP in l2_blob
    for name in CAST:
        assert name in l2.body_text, f"{name} should be introduced in Lesson 2's intro"
    for first_name in (n.split()[0] for n in CAST):
        assert first_name in l2_blob, f"{first_name} should appear across Lesson 2's tasks"


# --------------------------------------------------------------------------
# Rendered page: real interactive DOM
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_two_page_renders_all_five_activity_kinds(seeded):
    student = User.objects.create_user(
        email="m2l2-learner@example.com", password="x" * 14, is_verified=True
    )
    # Module 2 is sequentially locked behind Module 1 (a real 403, exercised
    # under test since DEBUG is forced off). Finish Module 1 to unlock it.
    m1 = Module.objects.get(order_index=1)
    for lesson in m1.lessons.order_by("lesson_number"):
        g.complete_lesson(student, lesson)
    QuizResult.objects.create(
        user=student, quiz=Quiz.objects.get(module=m1),
        attempt_number=1, score=100, passed=True,
    )
    g.refresh_profile(student)

    client = Client()
    client.force_login(student)
    html = client.get(
        reverse("learn:lesson", args=[2, 2]), HTTP_HOST="127.0.0.1"
    ).content.decode()
    for kind in ("SORT", "MAILSORT", "SEQUENCE", "CLASSIFY", "BRANCH"):
        assert f'data-activity-kind="{kind}"' in html, f"{kind} activity missing from Lesson 2"
    assert "<img" not in html
