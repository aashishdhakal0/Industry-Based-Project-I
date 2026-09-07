"""Module 5 (Firewall & Network Defence): understand it, then apply it.

Pins the restructured shape against order_index=5: Lesson 1 TEACHES (four reading
CONCEPT panels, each with a real visual, two of them the "watch it unfold"
animated heroes) plus one comprehension check on default-deny. Lesson 2 APPLIES
(the signature FIREWALL rule-reading activity, CLASSIFY zones, a picture CHECK,
NETMAP weaknesses, and a default-deny SORT). Plus the universal quality checks:
activities are well-formed and solvable, the quiz is valid and split across the
two lessons, the voice is em-dash-free, the ground is covered, and a full journey
reaches the module-complete moment.
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
    2: ["FIREWALL", "CLASSIFY", "CHECK", "NETMAP", "SORT"],
}
ACTIVITY_KINDS = {
    "SORT", "MAILSORT", "CLASSIFY", "BRANCH", "SEQUENCE", "SPOT",
    "HARDEN", "NETMAP", "RESPOND", "FIREWALL", "TABLETOP",
}
# Real visuals this module teaches from (diagram keys plus the two animated heroes).
FIGURES = {"firewall-flow", "segment-flow", "firewall", "segmentation"}
HEROES = {"firewall-flow", "segment-flow"}
L1_DIAGRAMS = {
    "the-firewall": "firewall",
    "defence-in-depth": "defence-in-depth",
    "segmentation": "segmentation",
    "remote-access": "vpn-tunnel",
}
DASHES = ("—", "–")


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=5)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


def _visual(task):
    return (task.diagram_key or (task.payload or {}).get("hero", "")
            or (task.image or {}).get("src", ""))


# --- shape: L1 teaches, L2 applies -----------------------------------------


@pytest.mark.django_db
def test_module_five_is_two_lessons_five_tasks(seeded):
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
        assert _visual(t), f"L1 task {t.task_key} has no teaching visual"


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
def test_uses_the_defence_figures_including_animated_heroes(seeded):
    used = set()
    for t in LessonTask.objects.filter(lesson__module=seeded):
        v = _visual(t)
        if v:
            used.add(v)
    assert FIGURES <= used, f"missing figures: {FIGURES - used}"
    # Lesson 1's four teaching panels use professional TECHNICAL DIAGRAMS
    # (firewall, defence-in-depth, segmentation, VPN tunnel), not stock photos.
    l1 = seeded.lessons.get(lesson_number=1)
    diagrams = {t.task_key: t.diagram_key for t in l1.tasks.filter(kind="CONCEPT")}
    assert diagrams == L1_DIAGRAMS
    for t in l1.tasks.filter(kind="CONCEPT"):
        assert not (t.image or {}).get("src"), f"{t.task_key} should be diagram-only"
    # Lesson 1 is theory-only: NO animated heroes there. Both "watch it unfold"
    # heroes now live on Lesson 2 practical tasks.
    l1_heroes = {(t.payload or {}).get("hero") for t in seeded.lessons.get(lesson_number=1).tasks.all()}
    assert not (HEROES & l1_heroes), f"Lesson 1 must have no animations: {HEROES & l1_heroes}"
    l2_heroes = {(t.payload or {}).get("hero") for t in seeded.lessons.get(lesson_number=2).tasks.all()}
    assert HEROES <= l2_heroes, f"animations must be relocated to L2: {HEROES - l2_heroes}"


# --- activity well-formedness (each solvable) ------------------------------


@pytest.mark.django_db
def test_firewall_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="FIREWALL")
    p = task.payload
    rule_ns = {r["n"] for r in p["rules"]}
    assert len(p["rules"]) >= 2 and any(r["action"] == "DENY" for r in p["rules"])
    assert len(p["traffic"]) >= 4
    for t in p["traffic"]:
        assert t["verdict"] in ("ALLOW", "BLOCK") and t["rule"] in rule_ns and t.get("text") and t.get("why")


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
def test_netmap_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="NETMAP")
    p = task.payload
    assert any(n["weak"] for n in p["nodes"]) and any(not n["weak"] for n in p["nodes"])
    for n in p["nodes"]:
        assert n.get("label") and n.get("why")


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
    for term in ("firewall", "default deny", "first", "segmentation", "zone",
                 "vpn", "remote desktop", "patch", "defence in depth"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey ------------------------------------------


@pytest.fixture
def learner_at_module_five(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner5@example.com", password="x" * 14, is_verified=True
    )
    for idx in (1, 2, 3, 4):
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
def test_full_interactive_module_five_journey(learner_at_module_five):
    client, student = learner_at_module_five
    m5 = Module.objects.get(order_index=5)

    first = m5.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[5, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page
    apply_page = client.get(reverse("learn:lesson", args=[5, 2])).content.decode()
    assert 'data-activity-kind="FIREWALL"' in apply_page

    for lesson in m5.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m5, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 50

    assert ProgressRecord.objects.filter(user=student, lesson__module=m5).count() == 2

    overview = client.get(reverse("learn:module", args=[5])).content.decode()
    assert "Take the quiz" in overview

    client.get(reverse("learn:quiz", args=[5]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids}
    client.post(reverse("learn:quiz_submit", args=[5]), answers)
    result = client.get(reverse("learn:quiz_result", args=[5])).content.decode()
    assert "passed" in result.lower()

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[5].complete is True
    assert progress[6].unlocked is True


@pytest.mark.django_db
def test_simulation_is_screen_driven(seeded):
    sim = seeded.simulation.decision_points
    assert sim["kind"] == "scenes"
    decisions = [s for s in sim["scenes"].values() if s.get("choices")]
    assert len(decisions) >= 2
    for sc in decisions:
        assert sc.get("screen") and sc["screen"].get("chrome") in ("browser", "window", "phone")
        assert sc["screen"].get("rows") or sc["screen"].get("email") or sc["screen"].get("items")
