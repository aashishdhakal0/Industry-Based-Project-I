"""Module 6 (Incident Response) meets the Module 1 gold standard, and completes
the six-module journey.

Mirrors the content contracts against order_index=6: every panel is deep reading
plus an interactive, points sum to 10, checks carry hints, the voice is
em-dash-free, and the quiz is a substantial, well-formed bank. Adds the new
`sequence` (order-the-phases) contract, and a full journey that finishes the
whole course: passing Module 6 completes every module, so the module-complete
moment offers the certificate rather than a next module.
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

# Every interactive "do it" kind now in the course (the new sequence included).
ACTIVITY_KINDS = {
    "SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH",
    "CLASSIFY", "MAILSORT", "HARDEN", "NETMAP", "SEQUENCE",
}
DASHES = ("—", "–")  # em-dash, en-dash: banned by the house voice


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=6)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


# --------------------------------------------------------------------------
# Shape: deep, interactive, points sum to 10
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_each_lesson_sums_to_ten_and_has_four_to_eight_panels(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        assert 4 <= len(tasks) <= 8, f"{lesson.title} has {len(tasks)} panels"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != 10 XP"


@pytest.mark.django_db
def test_every_panel_is_deep_reading_plus_interactive(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        kinds = {t.kind for t in tasks}
        assert "CHECK" in kinds, f"{lesson.title} has no check panel"
        assert kinds & ACTIVITY_KINDS, f"{lesson.title} has no hands-on activity"
        for t in tasks:
            words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
            assert words >= 40, f"{lesson.title}/{t.task_key} too thin ({words} words)"


@pytest.mark.django_db
def test_every_check_and_inline_check_is_well_formed_with_a_hint(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() >= 6
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
    assert len(inline) >= 4, "expected mid-panel checks woven across the module"
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
# Topic + activities: true to "Incident Response"
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_uses_its_planned_activity_set_including_the_new_sequence(seeded):
    kinds = set(
        LessonTask.objects.filter(lesson__module=seeded).values_list("kind", flat=True)
    )
    assert {"SEQUENCE", "CLASSIFY", "SORT", "BRANCH"} <= kinds, f"missing: {kinds}"


@pytest.mark.django_db
def test_uses_the_new_incident_response_diagrams(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert {"ir-lifecycle", "breach-notify"} <= keys


@pytest.mark.django_db
def test_sequence_activity_is_well_formed_with_a_clean_ordering(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="SEQUENCE")
    assert tasks.count() >= 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt"), f"{task.task_key} needs a prompt"
        steps = p["steps"]
        assert len(steps) >= 3, f"{task.task_key} needs several steps"
        for s in steps:
            assert s.get("label") and s.get("detail"), f"{task.task_key}/{s['id']} needs a label and detail"
            assert isinstance(s["order"], int), f"{task.task_key}/{s['id']} needs an integer order"
        orders = sorted(s["order"] for s in steps)
        # A clean, contiguous 1..N ordering with no gaps or duplicates.
        assert orders == list(range(1, len(steps) + 1)), f"{task.task_key} order is not a clean 1..N"


@pytest.mark.django_db
def test_branch_flagship_reaches_an_ending(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH")
    assert tasks.count() >= 1
    for task in tasks:
        p = task.payload
        assert p.get("start") and p.get("nodes")
        # At least one ending: a node with no choices.
        endings = [n for n in p["nodes"].values() if not n.get("choices")]
        assert endings, f"{task.task_key} has no ending node"
        # Every 'to' target points at a real node.
        for node in p["nodes"].values():
            for ch in node.get("choices", []):
                assert ch["to"] in p["nodes"], f"{task.task_key} choice points to a missing node"


@pytest.mark.django_db
def test_classify_and_sort_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY"):
        p = task.payload
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2 and len(p["events"]) >= 3
        for e in p["events"]:
            assert e["category"] in cats and e.get("text") and e.get("why")
        assert {e["category"] for e in p["events"]} == cats, "no category should be a dead decoy"
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="SORT"):
        p = task.payload
        bucket_ids = {b["id"] for b in p["buckets"]}
        assert len(p["items"]) >= 4
        for item in p["items"]:
            assert item["bucket"] in bucket_ids and item["why"]


# --------------------------------------------------------------------------
# Quiz: a substantial, well-formed bank for the engine and the AFE
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_quiz_is_a_substantial_evenly_spread_bank(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() == 10  # exactly ten, no random-draw bank
    per_lesson = Counter(
        quiz.questions.values_list("lesson_reference__lesson_number", flat=True)
    )
    for n in (1, 2, 3, 4):
        assert per_lesson[n] >= 2, f"lesson {n} is thin in the quiz bank ({per_lesson[n]})"


@pytest.mark.django_db
def test_every_question_is_well_formed_and_traces_to_a_lesson(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.all():
        answers = list(q.answers.all())
        assert len(answers) == 4, f"{q} needs four options"
        assert sum(1 for a in answers if a.correct_answer) == 1, f"{q} needs one correct"
        for a in answers:
            assert a.explanation_text.strip(), f"{q} option needs an explanation"
        assert q.lesson_reference_id in lesson_ids, f"{q} points outside Module 6"


# --------------------------------------------------------------------------
# The full journey finishes the course: passing Module 6 completes everything
# --------------------------------------------------------------------------


@pytest.fixture
def learner_at_module_six(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner6@example.com", password="x" * 14, is_verified=True
    )
    # Unlock Module 6 by completing Modules 1 to 5 (lessons + passed quizzes).
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
def test_full_journey_completes_the_course_and_offers_the_certificate(learner_at_module_six):
    client, student = learner_at_module_six
    m6 = Module.objects.get(order_index=6)

    first = m6.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[6, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page

    for lesson in m6.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m6, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 40

    assert ProgressRecord.objects.filter(user=student, lesson__module=m6).count() == 4

    # Take and pass the final quiz.
    client.get(reverse("learn:quiz", args=[6]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {
        f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids
    }
    client.post(reverse("learn:quiz_submit", args=[6]), answers)
    result = client.get(reverse("learn:quiz_result", args=[6])).content.decode()
    assert "passed" in result.lower()

    # Every module is now complete.
    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert all(progress[n].complete for n in range(1, 7)), "all six modules should be complete"

    # The final module's completion moment offers the certificate, not a next module.
    overview = client.get(reverse("learn:module", args=[6])).content.decode()
    assert "cy-moddone" in overview
    assert "Module 06 complete" in overview
    assert "See your certificate" in overview
    assert reverse("learn:certificate") in overview
    assert "Start Module" not in overview

    # And the certificate page now reports the course as earned.
    cert = client.get(reverse("learn:certificate")).content.decode()
    assert "earned" in cert.lower() or "complete" in cert.lower()
