"""Module 2 (Recognising Cyber Threats): two DEEP, HANDS-ON lessons.

Module 2 is deliberately two lessons, not four, and every panel is a practical
exercise rather than reading-then-MCQ. Each lesson keeps the five-panel room, but
the teaching happens THROUGH interaction: Lesson 1 is SORT, BRANCH, a picture
CHECK, MAILSORT, BRANCH; Lesson 2 is CLASSIFY, BRANCH, a picture CHECK, SEQUENCE,
BRANCH. This file pins that shape against order_index=2, the realistic threat
visuals, the well-formedness of every activity type (so each can actually be
solved and fire cy:solved), an em-dash-free voice, a balanced quiz bank feeding
the AFE, and a full interactive journey through the room to the module-complete
moment.
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

# The hands-on shape each lesson now follows (task 3 stays the picture CHECK).
LESSON_KINDS = {
    1: ["SORT", "BRANCH", "CHECK", "MAILSORT", "BRANCH"],
    2: ["CLASSIFY", "BRANCH", "CHECK", "SEQUENCE", "BRANCH"],
}
# The realistic picture visuals Module 2 reads from (two reused, two new).
# Schematic + realistic keys the module reads from.
PICTURE_DIAGRAMS = {"malware-family", "data-breach", "fake-update", "ransom-screen"}
# The realistic, screenshot-style visuals (each a picture-question the learner
# reads the answer from): the two picture CHECKs plus the four embedded ones.
REALISTIC_PICTURES = {
    "fake-update", "ransom-screen",          # the picture-question CHECKs (task 3)
    "download-trap", "attachment-exe",       # Lesson 1 embedded picture-questions
    "locked-files", "breach-email",          # Lesson 2 embedded picture-questions
}
DASHES = ("—", "–")  # em-dash, en-dash: banned by the house voice


def _check_options(task):
    """The option list of a task's picture-question, from its main CHECK or its
    inline_check, normalised to a list of {text, correct, explanation} dicts."""
    if task.kind == "CHECK" and task.payload.get("options"):
        return task.payload["question"], task.payload.get("hint", ""), task.payload["options"]
    ic = task.payload.get("inline_check")
    if ic:
        return ic.get("question", ""), ic.get("hint", ""), ic.get("options", [])
    return None, None, None


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
# Shape: two deep lessons, each the hands-on five-panel pattern, 40 XP
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_module_two_is_two_deep_lessons(seeded):
    assert seeded.lessons.count() == 2


@pytest.mark.django_db
def test_every_lesson_is_hands_on_in_the_expected_shape(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        tasks = list(lesson.tasks.order_by("order"))
        kinds = [t.kind for t in tasks]
        assert kinds == LESSON_KINDS[lesson.lesson_number], f"{lesson.title}: {kinds}"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != {POINTS_PER_LESSON} XP"
        # Task 3 is the picture-question CHECK and reads from a diagram.
        assert tasks[2].kind == "CHECK" and tasks[2].diagram_key, f"{lesson.title} task 3"
        # Every other panel is a genuine interactive activity, not a plain check.
        interactive = [t for t in tasks if t.kind != "CHECK"]
        assert len(interactive) == 4, f"{lesson.title} should be four activities + one picture check"


@pytest.mark.django_db
def test_every_panel_is_deep_reading(seeded):
    for lesson in seeded.lessons.order_by("lesson_number"):
        for t in lesson.tasks.order_by("order"):
            words = len(re.sub(r"<[^>]+>", " ", t.body or "").split())
            assert words >= 40, f"{lesson.title}/{t.task_key} too thin ({words} words)"


@pytest.mark.django_db
def test_each_lesson_has_at_least_two_picture_questions(seeded):
    """A picture-question is a panel that carries a realistic visual (diagram) AND
    a check that reads its answer from that image, whether the panel's main CHECK
    (task 3) or an inline_check embedded on an interactive drill. Every such check
    is well-formed: four options, exactly one correct, a hint, every option
    explained."""
    total = 0
    for lesson in seeded.lessons.order_by("lesson_number"):
        picture_questions = 0
        for task in lesson.tasks.order_by("order"):
            if not task.diagram_key:
                continue
            q, hint, opts = _check_options(task)
            if opts is None:
                continue  # a diagram with no question (schematic decoration) is fine
            # Only realistic, screenshot-style visuals count as picture-questions.
            if task.diagram_key not in REALISTIC_PICTURES:
                continue
            picture_questions += 1
            total += 1
            assert len(opts) == 4, f"{task.task_key} needs four options"
            assert sum(1 for o in opts if o["correct"]) == 1, f"{task.task_key} needs one correct"
            assert q and q.strip(), f"{task.task_key} needs a question"
            assert hint and hint.strip(), f"{task.task_key} needs a hint"
            for o in opts:
                assert o["explanation"].strip(), f"{task.task_key} option needs feedback"
        assert picture_questions >= 2, (
            f"{lesson.title} has only {picture_questions} picture-questions (need >= 2)"
        )
    assert total >= 6, f"expected at least six picture-questions across the module, got {total}"


@pytest.mark.django_db
def test_the_embedded_picture_questions_sit_alongside_the_drills(seeded):
    """The four new picture-questions are inline_checks embedded on interactive
    panels, so the drill is preserved and the picture-question is a required slot
    (diagram + inline_check on the same non-CHECK panel)."""
    embedded = [
        t for t in LessonTask.objects.filter(lesson__module=seeded)
        if t.kind != "CHECK" and t.diagram_key in REALISTIC_PICTURES and t.payload.get("inline_check")
    ]
    assert len(embedded) == 4, f"expected four embedded picture-questions, got {len(embedded)}"
    for t in embedded:
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


# --------------------------------------------------------------------------
# Every activity is well-formed, so it can actually be solved
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_uses_the_realistic_picture_visuals(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert PICTURE_DIAGRAMS <= keys, f"missing: {PICTURE_DIAGRAMS - keys}"
    # The realistic screenshot-style visuals are all present and seeded.
    assert REALISTIC_PICTURES <= keys, f"missing realistic visuals: {REALISTIC_PICTURES - keys}"


@pytest.mark.django_db
def test_sort_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="SORT")
    assert tasks.count() == 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt")
        bucket_ids = {b["id"] for b in p["buckets"]}
        assert len(bucket_ids) >= 3
        assert len(p["items"]) >= 4
        used = set()
        for item in p["items"]:
            assert item["bucket"] in bucket_ids, f"{task.task_key} item points at a missing bucket"
            assert item["text"] and item["why"], f"{task.task_key} item needs text and why"
            used.add(item["bucket"])


@pytest.mark.django_db
def test_classify_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY")
    assert tasks.count() == 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt")
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2
        assert len(p["events"]) >= 3
        for e in p["events"]:
            assert e["category"] in cats, f"{task.task_key}/{e.get('id')} category not offered"
            assert e.get("text") and e.get("why")
        used = {e["category"] for e in p["events"]}
        assert used == cats, f"{task.task_key} has unused categories {cats - used}"


@pytest.mark.django_db
def test_mailsort_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="MAILSORT")
    assert tasks.count() == 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt")
        assert len(p["emails"]) >= 4
        assert any(e["phish"] for e in p["emails"]), "an inbox needs at least one phish"
        assert any(not e["phish"] for e in p["emails"]), "an inbox needs at least one genuine"
        for e in p["emails"]:
            assert e.get("from") and e.get("subject") and e.get("preview") and e.get("why")


@pytest.mark.django_db
def test_sequence_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="SEQUENCE")
    assert tasks.count() == 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt")
        orders = sorted(s["order"] for s in p["steps"])
        assert orders == list(range(1, len(orders) + 1)), f"{task.task_key} orders not 1..n: {orders}"
        assert len(p["steps"]) >= 4
        for s in p["steps"]:
            assert s.get("label") and s.get("detail")


@pytest.mark.django_db
def test_branch_activities_are_solvable(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH")
    assert tasks.count() == 4  # two per lesson
    for task in tasks:
        p = task.payload
        assert p.get("prompt")
        nodes = p["nodes"]
        assert p["start"] in nodes, f"{task.task_key} start node missing"
        # Every node is reachable from start; collect endings and outcomes.
        seen, stack, endings, outcomes = set(), [p["start"]], [], set()
        while stack:
            nid = stack.pop()
            if nid in seen:
                continue
            seen.add(nid)
            node = nodes[nid]
            assert node.get("text"), f"{task.task_key}/{nid} needs scene text"
            choices = node.get("choices", [])
            if not choices:
                endings.append(nid)
            for c in choices:
                assert c.get("label") and c.get("feedback"), f"{task.task_key}/{nid} choice needs label + feedback"
                assert c["to"] in nodes, f"{task.task_key}/{nid} choice points at missing node {c['to']}"
                outcomes.add(c["outcome"])
                stack.append(c["to"])
        assert set(nodes) == seen, f"{task.task_key} has unreachable nodes {set(nodes) - seen}"
        assert "good" in outcomes and "bad" in outcomes, f"{task.task_key} needs good and bad outcomes"
        assert len(endings) >= 2, f"{task.task_key} needs at least two endings (a good and a bad)"


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

    # The first lesson renders as an interactive room with the new scripts, and
    # its opening panel mounts a real activity (the SORT drill).
    first = m2.lessons.order_by("lesson_number").first()
    page = client.get(reverse("learn:lesson", args=[2, first.lesson_number])).content.decode()
    assert "data-room" in page and "activities.js" in page
    assert 'data-activity-kind="SORT"' in page

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
