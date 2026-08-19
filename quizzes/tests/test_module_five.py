"""Module 5 (Firewall & Network Defence) meets the Module 1 gold standard.

Mirrors the content contracts against order_index=5: every panel is deep reading
plus an interactive, points sum to 10, checks carry hints, the voice is
em-dash-free, and the quiz is a substantial, well-formed bank. Adds the new
`netmap` (find-the-weaknesses) contract, and a full interactive journey proving
the room, banking, quiz gate and module-complete moment all fit together.
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

# The interactive "do it" kinds Module 5 draws on (the new netmap included).
ACTIVITY_KINDS = {
    "SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH",
    "CLASSIFY", "MAILSORT", "HARDEN", "NETMAP",
}
DASHES = ("—", "–")  # em-dash, en-dash: banned by the house voice


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=5)


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
# Topic + activities: true to "Firewall & Network Defence"
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_uses_its_planned_activity_set_including_the_new_netmap(seeded):
    kinds = set(
        LessonTask.objects.filter(lesson__module=seeded).values_list("kind", flat=True)
    )
    assert {"SORT", "CLASSIFY", "BRANCH", "NETMAP"} <= kinds, f"missing: {kinds}"


@pytest.mark.django_db
def test_uses_the_new_network_diagrams(seeded):
    keys = set(
        LessonTask.objects.filter(lesson__module=seeded)
        .exclude(diagram_key="")
        .values_list("diagram_key", flat=True)
    )
    assert {"firewall", "segmentation", "vpn-tunnel"} <= keys


@pytest.mark.django_db
def test_netmap_activity_is_well_formed_with_weak_and_safe_nodes(seeded):
    tasks = LessonTask.objects.filter(lesson__module=seeded, kind="NETMAP")
    assert tasks.count() >= 1
    for task in tasks:
        p = task.payload
        assert p.get("prompt"), f"{task.task_key} needs a prompt"
        nodes = p["nodes"]
        assert len(nodes) >= 4, f"{task.task_key} needs several nodes"
        for n in nodes:
            assert n.get("label") and n.get("detail") and n.get("why"), \
                f"{task.task_key}/{n['id']} needs a label, detail and why"
            assert isinstance(n["weak"], bool), f"{task.task_key}/{n['id']} needs a weak flag"
        weak = sum(1 for n in nodes if n["weak"])
        assert weak >= 1, f"{task.task_key} needs at least one weakness to find"
        assert weak < len(nodes), f"{task.task_key} needs at least one well-configured node too"


@pytest.mark.django_db
def test_classify_activity_is_well_formed_and_uses_every_category(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY"):
        p = task.payload
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2 and len(p["events"]) >= 3
        for e in p["events"]:
            assert e["category"] in cats and e.get("text") and e.get("why")
        assert {e["category"] for e in p["events"]} == cats, "no category should be a dead decoy"


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
        assert q.lesson_reference_id in lesson_ids, f"{q} points outside Module 5"


# --------------------------------------------------------------------------
# The full interactive journey: learn -> quiz -> pass -> Module 6 unlocks
# --------------------------------------------------------------------------


@pytest.fixture
def learner_at_module_five(client, db):
    User.objects.create_user(
        email="content-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    student = User.objects.create_user(
        email="learner5@example.com", password="x" * 14, is_verified=True
    )
    # Unlock Module 5 by completing Modules 1 to 4 (lessons + passed quizzes).
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

    for lesson in m5.lessons.order_by("lesson_number"):
        final = _work_through_lesson(client, m5, lesson)
        assert final["lesson_completed"] is True
        assert final["lesson_points_done"] == final["lesson_points_total"] == 40

    assert ProgressRecord.objects.filter(user=student, lesson__module=m5).count() == 4

    overview = client.get(reverse("learn:module", args=[5])).content.decode()
    assert "Take the quiz" in overview

    client.get(reverse("learn:quiz", args=[5]))
    ids = client.session["quiz_attempt"]["question_ids"]
    answers = {
        f"q{qid}": Answer.objects.get(question_id=qid, correct_answer=True).id for qid in ids
    }
    client.post(reverse("learn:quiz_submit", args=[5]), answers)
    result = client.get(reverse("learn:quiz_result", args=[5])).content.decode()
    assert "passed" in result.lower()

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[5].complete is True
    assert progress[6].unlocked is True

    overview = client.get(reverse("learn:module", args=[5])).content.decode()
    assert "cy-moddone" in overview
    assert "Module 05 complete" in overview
    assert "Start Module 6" in overview
    assert reverse("learn:module", args=[6]) in overview
