"""Module 1 is content-complete: interactive activities and a valid quiz bank.

These tests guard the *content contract* — that the seed produces genuine
interactive activities (each type's payload is well-formed and solvable) whose
points sum to a lesson's value, plus the end-of-module quiz bank the engine and
AFE rely on.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from modules.gamification import POINTS_PER_LESSON
from modules.models import LessonTask, Module
from quizzes.models import Answer

User = get_user_model()

# The interactive "do it" kinds — the weight of every lesson should be here.
ACTIVITY_KINDS = {"SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH"}


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=1)


# --------------------------------------------------------------------------
# Shape: interactive, weighted toward doing, points sum to 10
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_each_lesson_is_mostly_interactive_and_sums_to_ten(seeded):
    lessons = list(seeded.lessons.order_by("lesson_number"))
    assert len(lessons) == 4
    for lesson in lessons:
        tasks = list(lesson.tasks.order_by("order"))
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != 10 XP"
        activity_pts = sum(t.points for t in tasks if t.kind in ACTIVITY_KINDS)
        concept_pts = sum(t.points for t in tasks if t.kind == "CONCEPT")
        assert activity_pts >= 1, f"{lesson.title} has no interactive activity"
        # The doing outweighs the reading.
        assert activity_pts >= concept_pts, f"{lesson.title} is weighted toward reading"


@pytest.mark.django_db
def test_module_one_uses_all_five_activity_types(seeded):
    kinds = set(
        LessonTask.objects.filter(lesson__module=seeded).values_list("kind", flat=True)
    )
    assert ACTIVITY_KINDS <= kinds, f"missing activity types: {ACTIVITY_KINDS - kinds}"


# --------------------------------------------------------------------------
# Per-activity payload contracts — each must be well-formed and solvable
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_sort_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="SORT"):
        p = task.payload
        bucket_ids = {b["id"] for b in p["buckets"]}
        assert len(bucket_ids) >= 2, f"{task.task_key} needs at least two buckets"
        assert p["items"], f"{task.task_key} has no items"
        for item in p["items"]:
            assert item["bucket"] in bucket_ids, f"{task.task_key}: item in unknown bucket"
            assert item["text"] and item["why"], f"{task.task_key}: item missing text/why"
        # Solvable across buckets (not everything in one).
        used = {i["bucket"] for i in p["items"]}
        assert len(used) >= 2, f"{task.task_key}: all items in one bucket"


@pytest.mark.django_db
def test_inbox_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="INBOX"):
        p = task.payload
        assert p["parts"], f"{task.task_key} has no parts"
        bad = [pt for pt in p["parts"] if pt.get("bad")]
        assert bad, f"{task.task_key} has no suspicious part to find"
        for pt in p["parts"]:
            assert pt["text"] and pt["why"], f"{task.task_key}: part missing text/why"


@pytest.mark.django_db
def test_spot_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="SPOT"):
        p = task.payload
        assert p["fake"] in ("left", "right"), f"{task.task_key}: fake must be left/right"
        assert p["left"] and p["right"], f"{task.task_key}: needs both options"
        assert p["why"], f"{task.task_key}: needs an explanation"


@pytest.mark.django_db
def test_password_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="PASSWORD"):
        p = task.payload
        assert p.get("common"), f"{task.task_key} needs a common-password list"
        assert p.get("target"), f"{task.task_key} needs a target strength"


@pytest.mark.django_db
def test_branch_activities_are_well_formed_and_reach_an_ending(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH"):
        p = task.payload
        nodes = p["nodes"]
        assert p["start"] in nodes, f"{task.task_key}: start node missing"
        # Every choice points at a real node.
        for node in nodes.values():
            for choice in node["choices"]:
                assert choice["to"] in nodes, f"{task.task_key}: choice to unknown node"
        # There is at least one ending (a node with no choices).
        assert any(not n["choices"] for n in nodes.values()), f"{task.task_key}: no ending"


# --------------------------------------------------------------------------
# Coverage, diagram, quiz, idempotency
# --------------------------------------------------------------------------


def _all_strings(value):
    """Every string leaf inside a nested dict/list — the teaching surface."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _all_strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _all_strings(v)]
    return []


@pytest.mark.django_db
def test_module_one_covers_the_required_ground(seeded):
    parts = [l.body_text for l in seeded.lessons.all()]
    for t in LessonTask.objects.filter(lesson__module=seeded):
        parts.append(t.body)
        parts.extend(_all_strings(t.payload))
    corpus = " ".join(parts).lower()
    assert "confidentiality" in corpus and "integrity" in corpus and "availability" in corpus
    assert "network" in corpus
    assert "phishing" in corpus or "auspost" in corpus
    assert "human error" in corpus


@pytest.mark.django_db
def test_module_one_uses_the_cia_diagram(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert "cia-triad" in keys


@pytest.mark.django_db
def test_module_one_quiz_is_a_substantial_bank(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() >= 28
    # Evenly spread so any draw of 10 samples across the whole module.
    from collections import Counter

    per_lesson = Counter(
        quiz.questions.values_list("lesson_reference__lesson_number", flat=True)
    )
    for n in (1, 2, 3, 4):
        assert per_lesson[n] >= 5, f"lesson {n} is thin in the quiz bank"


@pytest.mark.django_db
def test_every_question_is_well_formed_for_the_engine_and_the_afe(seeded):
    for q in seeded.quiz.questions.all():
        answers = list(q.answers.all())
        assert len(answers) == 4, f"{q} does not have exactly four options"
        assert sum(1 for a in answers if a.correct_answer) == 1, f"{q} needs one correct option"
        for a in answers:
            assert a.explanation_text.strip(), f"{q} has an option with no explanation"


@pytest.mark.django_db
def test_every_question_traces_to_a_module_one_lesson(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.select_related("lesson_reference"):
        assert q.lesson_reference_id in lesson_ids, f"{q} references a lesson outside Module 1"


@pytest.mark.django_db
def test_the_seed_is_idempotent(seeded):
    """Re-running must update in place, not duplicate lessons, tasks or questions."""
    quiz = seeded.quiz

    def counts():
        return (
            seeded.lessons.count(),
            LessonTask.objects.filter(lesson__module=seeded).count(),
            quiz.questions.count(),
            Answer.objects.filter(question__quiz=quiz).count(),
        )

    before = counts()
    call_command("seed_learning_content")
    assert before == counts()


@pytest.mark.django_db
def test_each_lesson_weaves_concept_check_and_activity(seeded):
    """The richer format: every lesson mixes a concept, an inline check, and a
    hands-on activity — not read-then-answer."""
    for lesson in seeded.lessons.order_by("lesson_number"):
        kinds = set(lesson.tasks.values_list("kind", flat=True))
        assert "CONCEPT" in kinds, f"{lesson.title} has no concept intro"
        assert "CHECK" in kinds, f"{lesson.title} has no inline check"
        assert kinds & ACTIVITY_KINDS, f"{lesson.title} has no hands-on activity"
        assert lesson.tasks.count() >= 4, f"{lesson.title} is still thin"


@pytest.mark.django_db
def test_inline_check_tasks_are_well_formed(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() >= 6, "expected checks woven across the lessons"
    for task in checks:
        opts = task.payload.get("options", [])
        assert len(opts) == 4, f"{task.task_key} should have four options"
        assert sum(1 for o in opts if o["correct"]) == 1, f"{task.task_key} needs one correct"
        for o in opts:
            assert o["explanation"].strip(), f"{task.task_key} option needs feedback"
        assert task.payload.get("question"), f"{task.task_key} needs a question"
