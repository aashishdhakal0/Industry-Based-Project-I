"""Module 4 (Secure Communication Practices): two hands-on lessons.

Rebuilt to two lessons on the five-task room shape, with its own character: a
"before you hit send" checklist that runs through real send/share decisions,
driven by SORT, CLASSIFY, BRANCH, a HARDEN workspace pass, and picture CHECKs
that PROVE the point (an encrypted-vs-open message compare, a real-vs-risky share
link). This pins the shape against order_index=4, the figures, the
well-formedness of every activity, an em-dash-free voice, an exactly-ten quiz
split across the two lessons, and a full interactive journey.
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
    1: ["SORT", "BRANCH", "CHECK", "CLASSIFY", "BRANCH"],
    2: ["CLASSIFY", "BRANCH", "CHECK", "HARDEN", "BRANCH"],
}
FIGURES = {"msg-encrypted", "secure-share", "wifi-evil-twin", "scene-send"}
PICTURE_CHECKS = {"msg-encrypted", "secure-share"}
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


@pytest.mark.django_db
def test_module_four_is_two_hands_on_lessons(seeded):
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
def test_the_picture_question_checks_are_well_formed(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() == 2
    for task in checks:
        assert task.diagram_key in PICTURE_CHECKS, f"{task.task_key} unexpected visual {task.diagram_key}"
        opts = task.payload.get("options", [])
        assert len(opts) == 4 and sum(1 for o in opts if o["correct"]) == 1
        assert task.payload.get("question") and task.payload.get("hint", "").strip()
        for o in opts:
            assert o["explanation"].strip()


@pytest.mark.django_db
def test_task_two_has_the_people_scene_picture_question(seeded):
    """Lesson 1 Task 2 (the send/share scenario BRANCH) carries a people-scene
    figure and a picture-question read from it, alongside the decision drill."""
    t2 = seeded.lessons.get(lesson_number=1).tasks.order_by("order")[1]
    assert t2.kind == "BRANCH"
    assert t2.diagram_key == "scene-send"
    ic = t2.payload.get("inline_check")
    assert ic, "the scenario task should carry an inline picture-question"
    assert len(ic["options"]) == 4 and sum(1 for o in ic["options"] if o["correct"]) == 1
    assert ic.get("question") and ic.get("hint", "").strip()


@pytest.mark.django_db
def test_uses_the_figures(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="").values_list("diagram_key", flat=True)
    )
    assert FIGURES <= keys, f"missing figures: {FIGURES - keys}"


@pytest.mark.django_db
def test_inline_checks_are_well_formed(seeded):
    inline = [
        t for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("inline_check")
    ]
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


# --- activity well-formedness ---------------------------------------------


@pytest.mark.django_db
def test_sort_activity_is_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="SORT")
    assert tasks.count() == 1
    p = tasks.first().payload
    bucket_ids = {b["id"] for b in p["buckets"]}
    assert len(bucket_ids) >= 2 and len(p["items"]) >= 4
    for item in p["items"]:
        assert item["bucket"] in bucket_ids and item["text"] and item["why"]


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
def test_harden_activity_is_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="HARDEN")
    assert tasks.count() == 1
    p = tasks.first().payload
    assert len(p["steps"]) >= 3
    for s in p["steps"]:
        assert s.get("label") and sum(1 for o in s["options"] if o["correct"]) == 1
        for o in s["options"]:
            assert o.get("text") and o.get("why")


@pytest.mark.django_db
def test_branch_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH")
    assert tasks.count() == 4
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
    for term in ("encrypt", "padlock", "end-to-end", "sealed channel",
                 "evil twin", "vpn", "revoke", "hotspot"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey -----------------------------------------


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
    assert 'data-activity-kind="SORT"' in page

    for lesson in m4.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m4, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 40

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
