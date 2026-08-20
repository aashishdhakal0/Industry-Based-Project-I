"""Module 5 (Firewall & Network Defence): the flagship two-lesson build.

Pins the rebuilt module against order_index=5: two deep lessons on the five-task
room shape, each opening with a CSS animated "watch it unfold" sequence, the new
FIREWALL rule-reading activity, a network-segmentation CLASSIFY, the netmap
flagship, an em-dash-free voice, an exactly-ten quiz split across the two lessons,
and a full interactive journey to the module-complete moment.
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
    1: ["FIREWALL", "CLASSIFY", "CHECK", "BRANCH", "SORT"],
    2: ["CLASSIFY", "BRANCH", "CHECK", "NETMAP", "SORT"],
}
# The CSS animated sequences each lesson opens on (the video substitute).
ANIMATED_HEROES = {"firewall-flow", "segment-flow"}
# The picture-question CHECK visuals (task 3 of each lesson).
PICTURE_CHECKS = {"firewall", "segmentation"}
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


@pytest.mark.django_db
def test_module_five_is_two_deep_lessons(seeded):
    assert seeded.lessons.count() == 2
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        kinds = [t.kind for t in tasks]
        assert kinds == LESSON_KINDS[lesson.lesson_number], f"{lesson.title}: {kinds}"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != {POINTS_PER_LESSON} XP"
        assert tasks[2].kind == "CHECK" and tasks[2].diagram_key, f"{lesson.title} task 3"
        assert len([t for t in tasks if t.kind != "CHECK"]) == 4


@pytest.mark.django_db
def test_every_panel_is_deep_reading(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        for t in lesson.tasks.order_by("order"):
            words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
            assert words >= 40, f"{lesson.title}/{t.task_key} too thin ({words} words)"


@pytest.mark.django_db
def test_each_lesson_opens_with_an_animated_sequence(seeded):
    """The flagship "video substitute": lesson 1 opens on the firewall-flow
    animation, lesson 2 on the segment-flow animation, both carried as a task
    hero and rendered by the _diagram.html partials."""
    heroes = {
        t.payload.get("hero")
        for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("hero")
    }
    assert ANIMATED_HEROES <= heroes, f"missing animated heroes: {ANIMATED_HEROES - heroes}"


@pytest.mark.django_db
def test_the_picture_question_checks_are_well_formed(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() == 2  # one picture-question per lesson (task 3)
    for task in checks:
        assert task.diagram_key in PICTURE_CHECKS, f"{task.task_key} unexpected visual {task.diagram_key}"
        opts = task.payload.get("options", [])
        assert len(opts) == 4 and sum(1 for o in opts if o["correct"]) == 1
        assert task.payload.get("question") and task.payload.get("hint", "").strip()
        for o in opts:
            assert o["explanation"].strip()


@pytest.mark.django_db
def test_uses_the_network_diagrams(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="").values_list("diagram_key", flat=True)
    )
    assert {"firewall", "segmentation", "vpn-tunnel"} <= keys, f"missing figures: {keys}"


@pytest.mark.django_db
def test_inline_checks_are_well_formed(seeded):
    inline = [
        t for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("inline_check")
    ]
    assert len(inline) >= 2, "expected mid-panel checks woven through the module"
    for t in inline:
        ic = t.payload["inline_check"]
        assert len(ic["options"]) == 4 and sum(1 for o in ic["options"] if o["correct"]) == 1
        assert ic.get("question") and ic.get("hint", "").strip()


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


# --- activity well-formedness (so each can be solved) ---------------------


@pytest.mark.django_db
def test_the_firewall_activity_is_well_formed(seeded):
    """The new FIREWALL rule-reading activity: an ordered rule table (first match
    wins) and traffic that each cites a real rule for its verdict."""
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="FIREWALL")
    assert tasks.count() == 1
    p = tasks.first().payload
    assert p.get("prompt")
    rules = p["rules"]
    assert len(rules) >= 2
    rule_ns = {r["n"] for r in rules}
    assert len(rule_ns) == len(rules), "rule numbers must be unique"
    for r in rules:
        assert r["action"] in ("ALLOW", "DENY") and r.get("desc")
    assert len(p["traffic"]) >= 3
    for t in p["traffic"]:
        assert t["verdict"] in ("ALLOW", "BLOCK")
        assert t["rule"] in rule_ns, f"traffic cites unknown rule {t['rule']}"
        assert t.get("text") and t.get("why")


@pytest.mark.django_db
def test_the_segmentation_classify_uses_three_zones(seeded):
    """Lesson 2's segmentation scenario: every device is placed in a zone, and
    all three zones are genuinely used (no dead decoy category)."""
    task = seeded.lessons.get(lesson_number=2).tasks.get(task_key="zone-it")
    p = task.payload
    cats = {c["id"] for c in p["categories"]}
    assert len(cats) == 3, "segmentation should use three zones"
    assert len(p["events"]) >= 5
    for e in p["events"]:
        assert e["category"] in cats and e.get("text") and e.get("why")
    assert {e["category"] for e in p["events"]} == cats, "every zone must be used"


@pytest.mark.django_db
def test_classify_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY")
    assert tasks.count() == 2
    for task in tasks:
        p = task.payload
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2 and len(p["events"]) >= 4
        for e in p["events"]:
            assert e["category"] in cats and e.get("text") and e.get("why")
        assert {e["category"] for e in p["events"]} == cats, f"{task.task_key} has unused categories"


@pytest.mark.django_db
def test_sort_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="SORT")
    assert tasks.count() == 2
    for task in tasks:
        p = task.payload
        bucket_ids = {b["id"] for b in p["buckets"]}
        assert len(bucket_ids) >= 2 and len(p["items"]) >= 4
        for item in p["items"]:
            assert item["bucket"] in bucket_ids and item["text"] and item["why"]


@pytest.mark.django_db
def test_netmap_activity_is_well_formed(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="NETMAP")
    p = task.payload
    assert p.get("prompt")
    nodes = p["nodes"]
    assert len(nodes) >= 4
    for n in nodes:
        assert n.get("label") and n.get("why") and isinstance(n["weak"], bool)
    weak = sum(1 for n in nodes if n["weak"])
    assert 1 <= weak < len(nodes), "needs weaknesses to find and safe nodes too"


@pytest.mark.django_db
def test_branch_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH")
    assert tasks.count() == 2
    for task in tasks:
        p = task.payload
        assert p.get("prompt") and p["start"] in p["nodes"]
        nodes = p["nodes"]
        seen, stack, endings, outcomes = set(), [p["start"]], [], set()
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
        assert set(nodes) == seen, f"{task.task_key} unreachable nodes"
        assert "good" in outcomes and "bad" in outcomes and len(endings) >= 2


# --- quiz -----------------------------------------------------------------


@pytest.mark.django_db
def test_quiz_is_exactly_ten_split_across_two_lessons(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() == 10
    per_lesson = Counter(quiz.questions.values_list("lesson_reference__lesson_number", flat=True))
    for n in (1, 2):
        assert per_lesson[n] >= 2, f"lesson {n} thin in the bank ({per_lesson[n]})"


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
    for term in ("firewall", "default deny", "segment", "vpn", "remote",
                 "patch", "alert", "zone"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey -----------------------------------------


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
    assert 'data-activity-kind="FIREWALL"' in page

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
