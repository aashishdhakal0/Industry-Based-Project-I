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
# Module 1 is rebalanced toward DOING: hands-on activities are the centre of most
# panels, with a few short "apply it" checks and no pure-recall reading panels.
ACTIVITY_KINDS = {
    "SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH",
    "CLASSIFY", "MAILSORT", "HARDEN", "NETMAP", "SEQUENCE", "RESPOND",
}
# The classic five must always remain present in Module 1 (the reference module).
CLASSIC_FIVE = {"SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH"}


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
        # Interactive = hands-on activities plus checks (both give feedback);
        # reading = concept chunks. The doing should outweigh the reading.
        doing_pts = sum(t.points for t in tasks if t.kind in ACTIVITY_KINDS or t.kind == "CHECK")
        concept_pts = sum(t.points for t in tasks if t.kind == "CONCEPT")
        assert any(t.kind in ACTIVITY_KINDS for t in tasks), f"{lesson.title} has no hands-on activity"
        assert doing_pts >= concept_pts, f"{lesson.title} is weighted toward reading"


@pytest.mark.django_db
def test_module_one_uses_all_five_activity_types(seeded):
    kinds = set(
        LessonTask.objects.filter(lesson__module=seeded).values_list("kind", flat=True)
    )
    assert CLASSIC_FIVE <= kinds, f"missing activity types: {CLASSIC_FIVE - kinds}"


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
    assert quiz.questions.count() >= 40
    # Evenly spread so any draw of 10 samples across the whole module.
    from collections import Counter

    per_lesson = Counter(
        quiz.questions.values_list("lesson_reference__lesson_number", flat=True)
    )
    for n in (1, 2, 3, 4):
        assert per_lesson[n] >= 8, f"lesson {n} is thin in the quiz bank"


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
def test_every_lesson_is_doing_led(seeded):
    """The doing-centred standard: the interactive is the centre of each panel.
    Every panel has a tight setup (not a wall of text), every lesson has at least
    one genuine hands-on activity, and activity panels are the majority (doing
    outweighs reading-and-recall)."""
    import re

    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        activities = [t for t in tasks if t.kind in ACTIVITY_KINDS]
        others = [t for t in tasks if t.kind not in ACTIVITY_KINDS]  # checks / concepts
        assert activities, f"{lesson.title} has no hands-on activity"
        assert len(activities) >= len(others), f"{lesson.title} is not doing-led"
        for t in tasks:
            words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
            # Tight but real setup: enough to frame the task, not a wall of text.
            assert words >= 25, f"{lesson.title} / {t.task_key} has too little setup ({words} words)"


@pytest.mark.django_db
def test_classify_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY"):
        p = task.payload
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2 and len(p["events"]) >= 3, f"{task.task_key} too thin"
        for e in p["events"]:
            assert e["category"] in cats and e.get("text") and e.get("why")
        assert {e["category"] for e in p["events"]} == cats, f"{task.task_key} has a dead category"


@pytest.mark.django_db
def test_respond_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="RESPOND"):
        p = task.payload
        assert p.get("prompt"), f"{task.task_key} needs a prompt"
        assert len(p["situations"]) >= 2, f"{task.task_key} needs several situations"
        for s in p["situations"]:
            assert s.get("id") and s.get("text"), f"{task.task_key} situation needs id and text"
            assert len(s["options"]) >= 2, f"{task.task_key}/{s['id']} needs choices"
            goods = [o for o in s["options"] if o["outcome"] == "good"]
            assert len(goods) == 1, f"{task.task_key}/{s['id']} needs exactly one sound response"
            for o in s["options"]:
                assert o.get("text") and o.get("feedback"), f"{task.task_key}/{s['id']} option needs text + feedback"
                assert o["outcome"] in ("good", "risky", "bad")


@pytest.mark.django_db
def test_apply_it_check_tasks_are_well_formed(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.count() >= 3, "expected a few apply-it checks across the lessons"
    for task in checks:
        opts = task.payload.get("options", [])
        assert len(opts) == 4, f"{task.task_key} should have four options"
        assert sum(1 for o in opts if o["correct"]) == 1, f"{task.task_key} needs one correct"
        for o in opts:
            assert o["explanation"].strip(), f"{task.task_key} option needs feedback"
        assert task.payload.get("question"), f"{task.task_key} needs a question"


# --------------------------------------------------------------------------
# Gold-standard format: 5-8 tasks, ordering rule, hints, warm em-dash-free voice
# --------------------------------------------------------------------------

import json as _json

DASHES = ("—", "–")  # em-dash, en-dash


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


@pytest.mark.django_db
def test_each_lesson_has_four_to_eight_panels(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        n = lesson.tasks.count()
        assert 4 <= n <= 8, f"{lesson.title} has {n} panels (want 4 to 8)"


@pytest.mark.django_db
def test_never_two_concept_tasks_in_a_row(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        kinds = list(lesson.tasks.order_by("order").values_list("kind", flat=True))
        for a, b in zip(kinds, kinds[1:]):
            assert not (a == "CONCEPT" and b == "CONCEPT"), (
                f"{lesson.title}: two concept tasks in a row breaks the weight-toward-doing rule"
            )


@pytest.mark.django_db
def test_every_check_carries_a_hint(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.exists()
    for task in checks:
        assert task.payload.get("hint", "").strip(), f"{task.task_key} has no hint"


@pytest.mark.django_db
def test_lesson_content_has_no_em_dashes(seeded):
    """The house voice bans em/en-dashes. Enforced so every module that copies
    this reference stays in the same voice."""
    for task in LessonTask.objects.filter(lesson__module=seeded):
        blob = _content_blob(task)
        for d in DASHES:
            assert d not in blob, f"{task.task_key} contains a dash char {d!r}"


@pytest.mark.django_db
def test_module_one_uses_the_new_diagrams(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert {"two-factor", "defence-in-depth"} <= keys


@pytest.mark.django_db
def test_quiz_content_has_no_em_dashes(seeded):
    """Same voice rule as the lessons, applied to every question and explanation."""
    for q in seeded.quiz.questions.all():
        blob = q.question_text + " " + " ".join(
            a.option_text + " " + a.explanation_text for a in q.answers.all()
        )
        for d in DASHES:
            assert d not in blob, f"quiz question {q.id} contains a dash char {d!r}"


@pytest.mark.django_db
def test_reseeding_prunes_stale_quiz_options(seeded):
    """A revised question must not leave old options behind (which could create a
    second 'correct' answer). Inject a stray option, re-seed, and it should go."""
    q = seeded.quiz.questions.first()
    from quizzes.models import Answer as A
    A.objects.create(question=q, option_text="STALE leftover option", correct_answer=True,
                     explanation_text="from an older version")
    assert q.answers.count() == 5
    call_command("seed_learning_content")
    q.refresh_from_db()
    assert q.answers.count() == 4
    assert q.answers.filter(correct_answer=True).count() == 1
