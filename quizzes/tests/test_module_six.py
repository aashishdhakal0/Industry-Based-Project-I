"""Module 6 (Incident Response): the tabletop-exercise flagship.

Pins the rebuilt module against order_index=6: two deep lessons on the five-task
room shape, built around the new TABLETOP activity and its live situation board.
One escalating incident (a Geelong dental practice hit by ransomware) runs across
both lessons, covering the full response lifecycle (detect, contain, eradicate,
recover, review) and the Privacy Act notification duty. Also pins the animated
heroes, an em-dash-free voice, an exactly-ten quiz split across the two lessons,
and a full interactive journey to module complete.
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
    1: ["TABLETOP", "CLASSIFY", "CHECK", "SEQUENCE", "BRANCH"],
    2: ["TABLETOP", "CLASSIFY", "CHECK", "SORT", "BRANCH"],
}
ANIMATED_HEROES = {"incident-escalation", "recovery-board"}
PICTURE_CHECKS = {"ir-lifecycle", "breach-notify"}
DASHES = ("—", "–")


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=6)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


@pytest.mark.django_db
def test_module_six_is_two_deep_lessons(seeded):
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
    heroes = {
        t.payload.get("hero")
        for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("hero")
    }
    assert ANIMATED_HEROES <= heroes, f"missing animated heroes: {ANIMATED_HEROES - heroes}"


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
def test_uses_the_lifecycle_and_law_diagrams(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="").values_list("diagram_key", flat=True)
    )
    assert {"ir-lifecycle", "breach-notify"} <= keys, f"missing figures: {keys}"


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


# --- the tabletop centrepiece ---------------------------------------------


@pytest.mark.django_db
def test_the_tabletop_activities_are_well_formed(seeded):
    """Both TABLETOP panels: a live situation board plus ordered stages, each
    stage giving the learner a sound option and applying board deltas that target
    real indicators."""
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="TABLETOP")
    assert tasks.count() == 2
    for task in tasks:
        p = task.payload
        assert p.get("prompt") and p.get("scenario")
        board = p["board"]
        assert len(board) >= 3
        board_ids = {b["id"] for b in board}
        for b in board:
            assert b.get("label") and b.get("value") and b["state"] in ("ok", "warn", "bad")
        stages = p["stages"]
        assert len(stages) >= 3
        for st in stages:
            assert st.get("phase") and st.get("prompt")
            opts = st["options"]
            assert len(opts) >= 2
            assert any(o["outcome"] == "good" for o in opts), f"{task.task_key} stage needs a sound option"
            for o in opts:
                assert o["outcome"] in ("good", "bad") and o.get("label") and o.get("consequence")
                for bid, delta in (o.get("board") or {}).items():
                    assert bid in board_ids, f"{task.task_key} board delta targets unknown {bid}"
                    assert delta.get("state") in ("ok", "warn", "bad")


@pytest.mark.django_db
def test_the_tabletop_covers_the_whole_response_lifecycle(seeded):
    """Across the two panels, the tabletop works the full lifecycle: detect,
    contain, eradicate, recover, review."""
    phases = []
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="TABLETOP"):
        phases += [st["phase"].lower() for st in task.payload["stages"]]
    joined = " ".join(phases)
    for phase in ("detect", "contain", "eradicate", "recover", "review"):
        assert phase in joined, f"the tabletop never reaches the {phase} phase"


@pytest.mark.django_db
def test_sequence_orders_the_six_phases(seeded):
    task = seeded.lessons.get(lesson_number=1).tasks.get(kind="SEQUENCE")
    steps = task.payload["steps"]
    assert len(steps) == 6
    assert sorted(s["order"] for s in steps) == [1, 2, 3, 4, 5, 6]
    for s in steps:
        assert s.get("label") and s.get("detail")


# --- the supporting activities --------------------------------------------


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
def test_sort_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="SORT")
    p = task.payload
    bucket_ids = {b["id"] for b in p["buckets"]}
    assert len(bucket_ids) >= 2 and len(p["items"]) >= 4
    for item in p["items"]:
        assert item["bucket"] in bucket_ids and item["text"] and item["why"]


@pytest.mark.django_db
def test_inline_checks_are_well_formed(seeded):
    inline = [
        t for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("inline_check")
    ]
    assert len(inline) >= 2
    for t in inline:
        ic = t.payload["inline_check"]
        assert len(ic["options"]) == 4 and sum(1 for o in ic["options"] if o["correct"]) == 1
        assert ic.get("question") and ic.get("hint", "").strip()


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
    for term in ("incident", "contain", "eradicat", "recover", "ransomware",
                 "notifiable", "oaic", "privacy act", "lifecycle"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey -----------------------------------------


@pytest.fixture
def learner_at_module_six(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner6@example.com", password="x" * 14, is_verified=True
    )
    for idx in (1, 2, 3, 4, 5):
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
def test_full_interactive_module_six_journey(learner_at_module_six):
    client, student = learner_at_module_six
    m6 = Module.objects.get(order_index=6)

    first = m6.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[6, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page
    assert 'data-activity-kind="TABLETOP"' in page

    for lesson in m6.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m6, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 40

    assert ProgressRecord.objects.filter(user=student, lesson__module=m6).count() == 2

    overview = client.get(reverse("learn:module", args=[6])).content.decode()
    assert "Take the quiz" in overview

    client.get(reverse("learn:quiz", args=[6]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids}
    client.post(reverse("learn:quiz_submit", args=[6]), answers)
    result = client.get(reverse("learn:quiz_result", args=[6])).content.decode()
    assert "passed" in result.lower()

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[6].complete is True
