"""Module 2 (Recognising Cyber Threats): two DEEP lessons on the house standard.

Module 2 is deliberately two lessons, not four, each carrying the weight of the
old pairs. Both follow the same five-task room shape as Module 1's rebuilt
lessons: a Core CHECK, a real-world RESPOND, a realistic picture-question CHECK,
a mixed QUIZSET, and an applied CHECK. This file pins that shape against
order_index=2, the realistic threat visuals, the deep bodies, an em-dash-free
voice, a balanced quiz bank feeding the AFE, and a full interactive journey that
proves the room, the points banking, the quiz gate and the module-complete
moment all fit together for the second module too.
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

# The five-task house pattern every rebuilt lesson follows.
FIVE_TASK_PATTERN = ["CHECK", "RESPOND", "CHECK", "QUIZSET", "CHECK"]
# The realistic picture visuals Module 2 reads from (two reused, two new).
PICTURE_DIAGRAMS = {"malware-family", "data-breach", "fake-update", "ransom-screen"}
DASHES = ("—", "–")  # em-dash, en-dash: banned by the house voice


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=2)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


# --------------------------------------------------------------------------
# Shape: exactly two deep lessons, each the five-task pattern summing to 40 XP
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_module_two_is_two_deep_lessons(seeded):
    assert seeded.lessons.count() == 2


@pytest.mark.django_db
def test_every_lesson_follows_the_five_task_format(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        assert [t.kind for t in tasks] == FIVE_TASK_PATTERN, f"{lesson.title}: {[t.kind for t in tasks]}"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != {POINTS_PER_LESSON} XP"
        # The picture-question sits at task three and reads from a diagram.
        assert tasks[2].diagram_key, f"{lesson.title} task 3 has no diagram"


@pytest.mark.django_db
def test_every_panel_is_deep_reading(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        for t in lesson.tasks.order_by("order"):
            words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
            assert words >= 40, f"{lesson.title}/{t.task_key} too thin ({words} words)"


@pytest.mark.django_db
def test_every_check_and_inline_check_is_well_formed_with_a_hint(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() == 6  # three CHECK panels per lesson
    for task in checks:
        opts = task.payload.get("options", [])
        assert len(opts) == 4, f"{task.task_key} needs four options"
        assert sum(1 for o in opts if o["correct"]) == 1, f"{task.task_key} needs one correct"
        assert task.payload.get("question"), f"{task.task_key} needs a question"
        assert task.payload.get("hint", "").strip(), f"{task.task_key} needs a hint"
        for o in opts:
            assert o["explanation"].strip(), f"{task.task_key} option needs feedback"

    inline = [
        t for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.payload.get("inline_check")
    ]
    assert len(inline) >= 2, "expected mid-panel checks woven across the module"
    for t in inline:
        ic = t.payload["inline_check"]
        assert ic.get("question") and ic.get("hint", "").strip()
        assert len(ic["options"]) == 4 and sum(1 for o in ic["options"] if o["correct"]) == 1


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


# --------------------------------------------------------------------------
# Activities: the realistic picture visuals, respond and quizset
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_uses_the_realistic_picture_visuals(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert PICTURE_DIAGRAMS <= keys, f"missing: {PICTURE_DIAGRAMS - keys}"


@pytest.mark.django_db
def test_respond_activities_are_well_formed(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="RESPOND")
    assert tasks.count() == 2  # one per lesson
    for task in tasks:
        p = task.payload
        assert p.get("prompt"), f"{task.task_key} needs a prompt"
        assert len(p["situations"]) >= 3, f"{task.task_key} needs several situations"
        for s in p["situations"]:
            assert s.get("text"), f"{task.task_key}/{s.get('id')} needs text"
            goods = [o for o in s["options"] if o["outcome"] == "good"]
            assert len(goods) == 1, f"{task.task_key}/{s['id']} needs exactly one good option"
            for o in s["options"]:
                assert o.get("feedback", "").strip(), f"{task.task_key}/{s['id']} option needs feedback"


@pytest.mark.django_db
def test_quizset_activities_are_well_formed(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="QUIZSET")
    assert tasks.count() == 2  # one per lesson
    for task in tasks:
        qs = task.payload["questions"]
        assert 3 <= len(qs) <= 4, f"{task.task_key} needs three or four questions"
        types = {q["type"] for q in qs}
        assert len(types) >= 3, f"{task.task_key} needs a mix of question types ({types})"
        for q in qs:
            if q["type"] == "mcq":
                assert sum(1 for o in q["options"] if o[1]) == 1
                for o in q["options"]:
                    assert o[2].strip(), f"{task.task_key} mcq option needs an explanation"
            elif q["type"] == "truefalse":
                assert isinstance(q["answer"], bool) and q.get("why", "").strip()
            elif q["type"] == "fill":
                assert q.get("answer", "").strip()
            elif q["type"] == "match":
                assert len(q["pairs"]) >= 2


# --------------------------------------------------------------------------
# Quiz: a substantial, balanced bank for the engine and the AFE
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_quiz_is_a_substantial_balanced_bank(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() >= 40
    per_lesson = Counter(
        quiz.questions.values_list("lesson_reference__lesson_number", flat=True)
    )
    for n in (1, 2):
        assert per_lesson[n] >= 15, f"lesson {n} is thin in the quiz bank ({per_lesson[n]})"


@pytest.mark.django_db
def test_every_question_is_well_formed_and_traces_to_a_lesson(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.all():
        answers = list(q.answers.all())
        assert len(answers) == 4, f"{q} needs four options"
        assert sum(1 for a in answers if a.correct_answer) == 1, f"{q} needs one correct"
        for a in answers:
            assert a.explanation_text.strip(), f"{q} option needs an explanation"
        assert q.lesson_reference_id in lesson_ids, f"{q} points outside Module 2"


@pytest.mark.django_db
def test_the_module_covers_its_planned_topics(seeded):
    corpus = " ".join(
        (t.body or "") + _json.dumps(t.payload or {})
        for t in LessonTask.objects.filter(lesson__module=seeded)
    ).lower()
    for term in ("malware", "worm", "trojan", "spyware", "ransomware",
                 "confidentiality", "availability", "optus", "medibank"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --------------------------------------------------------------------------
# The full interactive journey: learn -> quiz -> pass -> Module 3 unlocks
# --------------------------------------------------------------------------


@pytest.fixture
def learner_at_module_two(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner2@example.com", password="x" * 14, is_verified=True
    )
    # Unlock Module 2 by completing Module 1 (lessons + a passed quiz).
    m1 = Module.objects.get(order_index=1)
    for lesson in m1.lessons.order_by("lesson_number"):
        g.complete_lesson(student, lesson)
    QuizResult.objects.create(
        user=student, quiz=Quiz.objects.get(module=m1),
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
def test_full_interactive_module_two_journey(learner_at_module_two):
    client, student = learner_at_module_two
    m2 = Module.objects.get(order_index=2)

    # The first lesson renders as an interactive room with the new scripts.
    first = m2.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[2, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page

    # Work through both deep lessons task by task; each banks on its last task.
    for lesson in m2.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m2, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 40

    assert ProgressRecord.objects.filter(user=student, lesson__module=m2).count() == 2

    # The overview now offers the quiz.
    overview = client.get(reverse("learn:module", args=[2])).content.decode()
    assert "Take the quiz" in overview

    # Take and pass the quiz.
    client.get(reverse("learn:quiz", args=[2]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {
        f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids
    }
    client.post(reverse("learn:quiz_submit", args=[2]), answers)
    result = client.get(reverse("learn:quiz_result", args=[2])).content.decode()
    assert "passed" in result.lower()

    # Module 2 is complete and Module 3 has unlocked.
    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[2].complete is True
    assert progress[3].unlocked is True

    # The completion moment points on to Module 3.
    overview = client.get(reverse("learn:module", args=[2])).content.decode()
    assert "cy-moddone" in overview
    assert "Module 02 complete" in overview
    assert "Start Module 3" in overview
    assert reverse("learn:module", args=[3]) in overview
