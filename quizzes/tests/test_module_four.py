"""Module 4 (Secure Communication Practices): understand it, then apply it.

Pins the restructured shape against order_index=4: Lesson 1 TEACHES (four reading
CONCEPT panels, each with a real visual: encryption, the padlock and end-to-end,
sharing safely, and staying private on the move) plus one light comprehension
check on an insecure send. Lesson 2 APPLIES (sort encrypted vs open, judge safe
shares from leaks, read a share-settings screen, work a share decision, and
harden a mobile workspace). Plus the universal quality checks: activities are
well-formed and solvable, the quiz is valid and split across the two lessons, the
voice is em-dash-free, the ground is covered, and a full journey reaches the
module-complete moment.
"""

import json as _json
import re
from collections import Counter

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules import gamification as g
from modules.gamification import POINTS_PER_LESSON
from modules.models import LessonTask, Module, ProgressRecord
from quizzes.models import Answer, Quiz, QuizResult

User = get_user_model()

LESSON_KINDS = {
    1: ["CONCEPT", "CONCEPT", "CONCEPT", "CONCEPT", "CHECK"],
    2: ["SORT", "CLASSIFY", "CHECK", "BRANCH", "HARDEN"],
}
ACTIVITY_KINDS = {
    "SORT", "MAILSORT", "CLASSIFY", "BRANCH", "SEQUENCE", "SPOT",
    "HARDEN", "NETMAP", "RESPOND", "FIREWALL", "TABLETOP",
}
FIGURES = {"msg-encrypted", "secure-bars", "secure-share", "vpn-tunnel", "compose-send", "wifi-evil-twin"}
DASHES = ("—", "–")


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=4)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


def _has_visual(task):
    return (bool(task.diagram_key) or bool((task.payload or {}).get("hero"))
            or bool((task.image or {}).get("src")))


# --- shape: L1 teaches, L2 applies -----------------------------------------


@pytest.mark.django_db
def test_module_four_is_two_lessons_five_tasks(seeded):
    assert seeded.lessons.count() == 2
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        assert [t.kind for t in tasks] == LESSON_KINDS[lesson.lesson_number], f"{lesson.title}"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != {POINTS_PER_LESSON} XP"


@pytest.mark.django_db
def test_lesson_one_is_a_teaching_lesson(seeded):
    tasks = list(seeded.lessons.get(lesson_number=1).tasks.order_by("order"))
    assert len([t for t in tasks if t.kind == "CONCEPT"]) >= 3
    assert len([t for t in tasks if t.kind == "CHECK"]) <= 2
    assert not [t for t in tasks if t.kind in ACTIVITY_KINDS], "L1 teaches; activities belong in L2"
    for t in tasks:
        assert _has_visual(t), f"L1 task {t.task_key} has no teaching visual"


@pytest.mark.django_db
def test_lesson_two_is_an_apply_lesson(seeded):
    tasks = list(seeded.lessons.get(lesson_number=2).tasks.order_by("order"))
    assert len([t for t in tasks if t.kind in ACTIVITY_KINDS]) >= 3
    assert not [t for t in tasks if t.kind == "CONCEPT"]
    assert [t for t in tasks if t.kind == "CHECK" and t.diagram_key], "L2 needs a picture question"


@pytest.mark.django_db
def test_every_teaching_panel_has_enough_substance(seeded):
    """Lesson 1 reading panels are substantial; the closing CHECK is exempt."""
    for t in seeded.lessons.get(lesson_number=1).tasks.filter(kind="CONCEPT").order_by("order"):
        words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
        assert words >= 60, f"{t.task_key} is thin for a teaching panel ({words} words)"


@pytest.mark.django_db
def test_uses_the_secure_comms_figures(seeded):
    # Lesson 1's four teaching panels use professional TECHNICAL DIAGRAMS
    # (encryption compare, open-vs-encrypted, share-link and Wi-Fi mockups).
    l1 = seeded.lessons.get(lesson_number=1)
    diagrams = {t.task_key: t.diagram_key for t in l1.tasks.filter(kind="CONCEPT")}
    assert diagrams == {
        "encryption": "encryption",
        "padlock-and-e2e": "msg-encrypted",
        "sharing-safely": "secure-share",
        "on-the-move": "wifi-evil-twin",
    }
    for t in l1.tasks.filter(kind="CONCEPT"):
        assert not (t.image or {}).get("src"), f"{t.task_key} should be diagram-only"
    # The readable picture-question mockups remain (scene-send check, secure-share
    # + wifi-evil-twin in Lesson 2).
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="").values_list("diagram_key", flat=True)
    )
    assert {"compose-send", "secure-share", "wifi-evil-twin"} <= keys, f"mockups missing: {keys}"


# --- activity well-formedness (each solvable) ------------------------------


@pytest.mark.django_db
def test_sort_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="SORT")
    p = task.payload
    bucket_ids = {b["id"] for b in p["buckets"]}
    assert len(bucket_ids) >= 2 and len(p["items"]) >= 4
    for item in p["items"]:
        assert item["bucket"] in bucket_ids and item["text"] and item["why"]
    assert len({i["bucket"] for i in p["items"]}) >= 2


@pytest.mark.django_db
def test_classify_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="CLASSIFY")
    p = task.payload
    cats = {c["id"] for c in p["categories"]}
    assert len(cats) >= 2 and len(p["events"]) >= 4
    for e in p["events"]:
        assert e["category"] in cats and e.get("text") and e.get("why")
    assert {e["category"] for e in p["events"]} == cats, "no dead category"


@pytest.mark.django_db
def test_branch_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="BRANCH")
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
            outcomes.add(c["outcome"]); stack.append(c["to"])
        if not node.get("choices"):
            endings.append(nid)
    assert set(nodes) == seen, "unreachable nodes"
    assert "good" in outcomes and "bad" in outcomes and len(endings) >= 2


@pytest.mark.django_db
def test_harden_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="HARDEN")
    p = task.payload
    assert len(p["steps"]) >= 3
    for step in p["steps"]:
        assert step.get("label") and step.get("risk")
        assert sum(1 for o in step["options"] if o["correct"]) == 1
        for o in step["options"]:
            assert o.get("text") and o.get("why")


@pytest.mark.django_db
def test_the_picture_checks_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="CHECK"):
        assert task.diagram_key, f"{task.task_key} picture check needs a visual"
        opts = task.payload.get("options", [])
        assert len(opts) == 4 and sum(1 for o in opts if o["correct"]) == 1
        assert task.payload.get("question") and task.payload.get("hint", "").strip()
        for o in opts:
            assert o["explanation"].strip()


# --- voice, quiz, coverage -------------------------------------------------


@pytest.mark.django_db
def test_lesson_and_quiz_content_have_no_em_dashes(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded):
        blob = _content_blob(task)
        for d in DASHES:
            assert d not in blob, f"{task.task_key} contains {d!r}"
    for q in seeded.quiz.questions.all():
        blob = q.question_text + " " + " ".join(
            a.option_text + " " + a.explanation_text for a in q.answers.all()
        )
        for d in DASHES:
            assert d not in blob, f"quiz question {q.id} contains {d!r}"


@pytest.mark.django_db
def test_quiz_is_exactly_ten_split_across_two_lessons(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70 and quiz.questions.count() == 10
    per_lesson = Counter(quiz.questions.values_list("lesson_reference__lesson_number", flat=True))
    for n in (1, 2):
        assert per_lesson[n] >= 2, f"lesson {n} thin ({per_lesson[n]})"


@pytest.mark.django_db
def test_every_question_is_well_formed_and_traces_to_a_lesson(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.all():
        answers = list(q.answers.all())
        assert len(answers) == 4 and sum(1 for a in answers if a.correct_answer) == 1
        for a in answers:
            assert a.explanation_text.strip()
        assert q.lesson_reference_id in lesson_ids


@pytest.mark.django_db
def test_the_module_covers_its_planned_topics(seeded):
    corpus = " ".join(
        (t.body or "") + _json.dumps(t.payload or {})
        for t in LessonTask.objects.filter(lesson__module=seeded)
    ).lower()
    for term in ("encrypt", "padlock", "end-to-end", "vpn", "evil twin",
                 "public wi-fi", "permissioned", "revoke"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey ------------------------------------------


@pytest.fixture
def learner_at_module_four(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner4@example.com", password="x" * 14, is_verified=True
    )
    for idx in (1, 2, 3):
        module = Module.objects.get(order_index=idx)
        for lesson in module.lessons.order_by("lesson_number"):
            g.complete_lesson(student, lesson)
        QuizResult.objects.create(
            user=student, quiz=Quiz.objects.get(module=module),
            attempt_number=1, score=100, passed=True,
        )
    g.refresh_profile(student)
    client.force_login(student)
    return client, student


def _work_through_lesson(client, module, lesson):
    result = None
    for task in lesson.tasks.order_by("order"):
        resp = client.post(
            reverse("learn:complete_task", args=[module.order_index, lesson.lesson_number]),
            {"task": task.id},
        )
        assert resp.status_code == 200
        result = resp.json()
    return result


@pytest.mark.django_db
def test_full_interactive_module_four_journey(learner_at_module_four):
    client, student = learner_at_module_four
    m4 = Module.objects.get(order_index=4)

    first = m4.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[4, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page
    apply_page = client.get(reverse("learn:lesson", args=[4, 2])).content.decode()
    assert 'data-activity-kind="SORT"' in apply_page

    for lesson in m4.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m4, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 50

    assert ProgressRecord.objects.filter(user=student, lesson__module=m4).count() == 2

    overview = client.get(reverse("learn:module", args=[4])).content.decode()
    assert "Take the quiz" in overview

    client.get(reverse("learn:quiz", args=[4]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids}
    client.post(reverse("learn:quiz_submit", args=[4]), answers)
    result = client.get(reverse("learn:quiz_result", args=[4])).content.decode()
    assert "passed" in result.lower()

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[4].complete is True
    assert progress[5].unlocked is True


ANIMATIONS = {
    "data-journey", "infection-spread", "phish-unfold", "eavesdrop",
    "firewall-flow", "segment-flow", "incident-escalation", "recovery-board", "net-scene",
}


@pytest.mark.django_db
def test_lesson_one_is_theory_only_and_sim_is_screen_driven(seeded):
    # Lesson 1 carries no animation (they live in Lesson 2).
    l1_heroes = {(t.payload or {}).get("hero") for t in seeded.lessons.get(lesson_number=1).tasks.all()}
    assert not (ANIMATIONS & l1_heroes), f"Lesson 1 must have no animations: {ANIMATIONS & l1_heroes}"
    # The simulation is scene-based and every decision reads a device-framed screen.
    sim = seeded.simulation.decision_points
    assert sim["kind"] == "scenes"
    decisions = [s for s in sim["scenes"].values() if s.get("choices")]
    assert len(decisions) >= 2
    for sc in decisions:
        assert sc.get("screen") and sc["screen"].get("chrome") in ("browser", "window", "phone")
        assert sc["screen"].get("rows") or sc["screen"].get("email") or sc["screen"].get("items")
