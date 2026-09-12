"""Module 6 (Incident Response): understand it, then apply it.

Pins the restructured shape against order_index=6: Lesson 1 TEACHES the whole
discipline (four reading CONCEPT panels, two carrying the animated heroes, plus
one comprehension check on the order of the phases). Lesson 2 APPLIES it through
the two signature TABLETOP exercises on a live situation board, a first-move
CLASSIFY, a picture CHECK, and ordering the phases. One escalating incident (a
Geelong dental practice hit by ransomware) runs across both lessons, covering the
full lifecycle and the Privacy Act notification duty. Plus the universal quality
checks: activities are well-formed and solvable, the quiz is valid and split, the
voice is em-dash-free, the ground is covered, and a full journey reaches module
complete (finishing the whole six-module course).
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
    2: ["TABLETOP", "CLASSIFY", "CHECK", "SEQUENCE", "TABLETOP"],
}
ACTIVITY_KINDS = {
    "SORT", "MAILSORT", "CLASSIFY", "BRANCH", "SEQUENCE", "SPOT",
    "HARDEN", "NETMAP", "RESPOND", "FIREWALL", "TABLETOP",
}
ANIMATED_HEROES = {"incident-escalation", "recovery-board"}
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


def _visual(task):
    return (task.diagram_key or (task.payload or {}).get("hero", "")
            or (task.image or {}).get("src", ""))


# --- shape: L1 teaches, L2 applies -----------------------------------------


@pytest.mark.django_db
def test_module_six_is_two_lessons_five_tasks(seeded):
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
    # Most L1 panels carry a teaching visual; a concept panel that stands on its
    # text (the 'why the first hours matter' overview) may have none, rather than
    # a decorative filler image.
    assert len([t for t in tasks if _visual(t)]) >= 4


@pytest.mark.django_db
def test_lesson_two_is_an_apply_lesson(seeded):
    tasks = list(seeded.lessons.get(lesson_number=2).tasks.order_by("order"))
    assert len([t for t in tasks if t.kind in ACTIVITY_KINDS]) >= 3
    assert not [t for t in tasks if t.kind == "CONCEPT"]
    assert [t for t in tasks if t.kind == "CHECK" and t.diagram_key], "L2 needs a picture question"
    assert len([t for t in tasks if t.kind == "TABLETOP"]) == 2, "L2 carries both tabletop exercises"


@pytest.mark.django_db
def test_every_teaching_panel_has_enough_substance(seeded):
    """Lesson 1 reading panels are substantial; the closing CHECK is exempt."""
    for t in seeded.lessons.get(lesson_number=1).tasks.filter(kind="CONCEPT").order_by("order"):
        words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
        assert words >= 60, f"{t.task_key} is thin for a teaching panel ({words} words)"


@pytest.mark.django_db
def test_lesson_one_uses_technical_diagrams(seeded):
    # Lesson 1's four teaching panels use professional TECHNICAL DIAGRAMS
    # (a first-hour timeline, the response lifecycle, a containment map and the
    # Notifiable Data Breaches flow), not stock photos.
    l1 = seeded.lessons.get(lesson_number=1)
    diagrams = {t.task_key: t.diagram_key for t in l1.tasks.filter(kind="CONCEPT")}
    assert diagrams == {
        "first-hours": "first-hours",
        "the-lifecycle": "ir-lifecycle",
        "detect-contain": "containment",
        "recover-and-law": "breach-notify",
    }
    for t in l1.tasks.filter(kind="CONCEPT"):
        assert not (t.image or {}).get("src"), f"{t.task_key} should be diagram-only"
    # The comprehension CHECK keeps its readable lifecycle diagram.
    assert l1.tasks.get(kind="CHECK").diagram_key == "ir-alert"


@pytest.mark.django_db
def test_animations_live_in_lesson_two_only(seeded):
    heroes = set()
    for t in LessonTask.objects.filter(lesson__module=seeded):
        h = (t.payload or {}).get("hero")
        if h:
            heroes.add(h)
    assert ANIMATED_HEROES <= heroes, f"missing animated heroes: {ANIMATED_HEROES - heroes}"
    # Lesson 1 is theory-only: both "watch it unfold" heroes live on Lesson 2's
    # tabletop exercises, not on a teaching panel.
    l1_heroes = {(t.payload or {}).get("hero") for t in seeded.lessons.get(lesson_number=1).tasks.all()}
    assert not (ANIMATED_HEROES & l1_heroes), f"Lesson 1 must have no animations: {ANIMATED_HEROES & l1_heroes}"
    l2_heroes = {(t.payload or {}).get("hero") for t in seeded.lessons.get(lesson_number=2).tasks.all()}
    assert ANIMATED_HEROES <= l2_heroes


# --- activity well-formedness (each solvable) ------------------------------


@pytest.mark.django_db
def test_both_tabletops_are_well_formed(seeded):
    tabletops = LessonTask.objects.filter(lesson__module=seeded, kind="TABLETOP")
    assert tabletops.count() == 2
    for task in tabletops:
        p = task.payload
        assert p.get("prompt") and p.get("scenario")
        board_ids = {b["id"] for b in p["board"]}
        assert len(p["board"]) >= 3 and len(p["stages"]) >= 3
        for stage in p["stages"]:
            assert stage.get("phase") and stage.get("prompt")
            assert sum(1 for o in stage["options"] if o["outcome"] == "good") == 1
            for o in stage["options"]:
                assert o.get("label") and o.get("consequence")
                # every board update targets a real board cell
                assert set((o.get("board") or {}).keys()) <= board_ids


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
def test_sequence_activity_is_solvable(seeded):
    task = seeded.lessons.get(lesson_number=2).tasks.get(kind="SEQUENCE")
    p = task.payload
    orders = sorted(s["order"] for s in p["steps"])
    assert orders == list(range(1, len(p["steps"]) + 1)), "orders must be a clean 1..n"
    for s in p["steps"]:
        assert s.get("label") and s.get("detail")


@pytest.mark.django_db
def test_the_picture_check_is_well_formed(seeded):
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
    for term in ("incident response", "containment", "eradicat", "recover",
                 "notifiable data breaches", "oaic", "privacy act", "serious harm",
                 "lessons learned"):
        assert term in corpus, f"expected the module to cover {term!r}"


# --- the full interactive journey ------------------------------------------


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
    apply_page = client.get(reverse("learn:lesson", args=[6, 2])).content.decode()
    assert 'data-activity-kind="TABLETOP"' in apply_page

    for lesson in m6.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m6, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 50

    assert ProgressRecord.objects.filter(user=student, lesson__module=m6).count() == 2

    overview = client.get(reverse("learn:module", args=[6])).content.decode()
    assert "Take the quiz" in overview

    client.get(reverse("learn:quiz", args=[6]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids}
    client.post(reverse("learn:quiz_submit", args=[6]), answers)
    result = client.get(reverse("learn:quiz_result", args=[6])).content.decode()
    assert "passed" in result.lower()

    # Module 6 is the last one: finishing it completes the whole course.
    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[6].complete is True
    assert all(progress[i].complete for i in range(1, 7)), "the whole course should now be complete"


@pytest.mark.django_db
def test_simulation_is_screen_driven(seeded):
    sim = seeded.simulation.decision_points
    assert sim["kind"] == "scenes"
    decisions = [s for s in sim["scenes"].values() if s.get("choices")]
    assert len(decisions) >= 2
    for sc in decisions:
        assert sc.get("screen") and sc["screen"].get("chrome") in ("browser", "window", "phone")
        assert sc["screen"].get("rows") or sc["screen"].get("email") or sc["screen"].get("items")
