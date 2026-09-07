"""Module 1 content contract — the "understand it, then apply it" reference shape.

Module 1 is the gold standard the others copy, so these tests pin the new shape:
Lesson 1 TEACHES (mostly reading CONCEPT panels, each with a real visual, and
only a light comprehension check), Lesson 2 APPLIES (hands-on, scenario-based
activities). Plus the universal quality checks: activity payloads are well-formed
and solvable, the quiz bank is valid and traces to the right lesson, the voice is
em-dash-free, and the seed is idempotent.
"""

import json as _json
from collections import Counter

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from modules.gamification import POINTS_PER_LESSON
from modules.models import LessonTask, Module
from quizzes.models import Answer

User = get_user_model()

# The interactive "do it" kinds — Lesson 2 (Apply it) is built from these.
ACTIVITY_KINDS = {
    "SORT", "INBOX", "SPOT", "PASSWORD", "BRANCH",
    "CLASSIFY", "MAILSORT", "HARDEN", "NETMAP", "SEQUENCE", "RESPOND",
    "QUIZSET", "FIREWALL", "TABLETOP",
}
DASHES = ("—", "–")


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="seed-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")
    return Module.objects.get(order_index=1)


def _content_blob(task):
    return (task.body or "") + _json.dumps(task.payload or {})


def _has_visual(task):
    # a real photo (image), a mockup diagram, or an animated hero all count
    return bool((task.image or {}).get("src")) or bool(task.diagram_key) or bool((task.payload or {}).get("hero"))


# --------------------------------------------------------------------------
# The new shape: L1 teaches, L2 applies, five tasks each, points sum to ten
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_two_lessons_five_tasks_each(seeded):
    lessons = list(seeded.lessons.order_by("lesson_number"))
    assert len(lessons) == 2
    for lesson in lessons:
        tasks = list(lesson.tasks.order_by("order"))
        assert len(tasks) == 5, f"{lesson.title} has {len(tasks)} tasks"
        assert sum(t.points for t in tasks) == POINTS_PER_LESSON, f"{lesson.title} != {POINTS_PER_LESSON} XP"


@pytest.mark.django_db
def test_lesson_one_is_a_teaching_lesson(seeded):
    """Lesson 1 UNDERSTAND IT: mostly reading CONCEPT panels (teaching), each with
    a real visual, and at most a couple of light comprehension checks."""
    tasks = list(seeded.lessons.get(lesson_number=1).tasks.order_by("order"))
    concepts = [t for t in tasks if t.kind == "CONCEPT"]
    checks = [t for t in tasks if t.kind == "CHECK"]
    assert len(concepts) >= 3, "Lesson 1 should be teaching-led (mostly CONCEPT panels)"
    assert len(checks) <= 2, "Lesson 1 keeps questions light (one or two checks)"
    assert not [t for t in tasks if t.kind in ACTIVITY_KINDS], \
        "Lesson 1 teaches; the hands-on activities belong in Lesson 2"
    # Every teaching panel earns its place with a visual.
    for t in tasks:
        assert _has_visual(t), f"L1 task {t.task_key} has no teaching visual"


@pytest.mark.django_db
def test_lesson_two_is_an_apply_lesson(seeded):
    """Lesson 2 APPLY IT: hands-on, scenario-based. Mostly interactive activities,
    with at least one read-the-image picture question."""
    tasks = list(seeded.lessons.get(lesson_number=2).tasks.order_by("order"))
    activities = [t for t in tasks if t.kind in ACTIVITY_KINDS]
    assert len(activities) >= 3, "Lesson 2 should be built from hands-on activities"
    assert not [t for t in tasks if t.kind == "CONCEPT"], "Lesson 2 applies; it should not be reading panels"
    # At least one picture-question (a CHECK carrying a visual).
    picture_checks = [t for t in tasks if t.kind == "CHECK" and t.diagram_key]
    assert picture_checks, "Lesson 2 needs at least one read-the-image picture question"


# --------------------------------------------------------------------------
# Per-activity payload contracts — each must be well-formed and solvable
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_sort_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="SORT"):
        p = task.payload
        bucket_ids = {b["id"] for b in p["buckets"]}
        assert len(bucket_ids) >= 2 and p["items"]
        for item in p["items"]:
            assert item["bucket"] in bucket_ids and item["text"] and item["why"]
        assert len({i["bucket"] for i in p["items"]}) >= 2, f"{task.task_key}: all items in one bucket"


@pytest.mark.django_db
def test_classify_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="CLASSIFY"):
        p = task.payload
        cats = {c["id"] for c in p["categories"]}
        assert len(cats) >= 2 and len(p["events"]) >= 3
        for e in p["events"]:
            assert e["category"] in cats and e.get("text") and e.get("why")
        assert {e["category"] for e in p["events"]} == cats, f"{task.task_key} has a dead category"


@pytest.mark.django_db
def test_branch_activities_are_well_formed_and_reach_an_ending(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="BRANCH"):
        p = task.payload
        nodes = p["nodes"]
        assert p["start"] in nodes
        seen, stack, outcomes, endings = set(), [p["start"]], set(), []
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


@pytest.mark.django_db
def test_harden_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="HARDEN"):
        p = task.payload
        assert p.get("prompt") and len(p["steps"]) >= 3
        for step in p["steps"]:
            assert step.get("label") and step.get("risk")
            assert sum(1 for o in step["options"] if o["correct"]) == 1
            for o in step["options"]:
                assert o.get("text") and o.get("why")


ANIMATIONS = {
    "data-journey", "infection-spread", "phish-unfold", "eavesdrop",
    "firewall-flow", "segment-flow", "incident-escalation", "recovery-board", "net-scene",
}


@pytest.mark.django_db
def test_lesson_one_is_theory_only_no_animations(seeded):
    """Lesson 1 teaches; every animation and drill lives in Lesson 2. No animated
    hero may sit on a Lesson 1 panel."""
    l1_heroes = {
        (t.payload or {}).get("hero")
        for t in seeded.lessons.get(lesson_number=1).tasks.all()
    }
    assert not (l1_heroes & ANIMATIONS), f"Lesson 1 must have no animations: {l1_heroes & ANIMATIONS}"
    # The 'watch your data travel' animation was relocated to Lesson 2.
    l2_heroes = {
        (t.payload or {}).get("hero")
        for t in seeded.lessons.get(lesson_number=2).tasks.all()
    }
    assert "data-journey" in l2_heroes


@pytest.mark.django_db
def test_respond_activities_are_well_formed(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded, kind="RESPOND"):
        p = task.payload
        assert p.get("prompt") and len(p["situations"]) >= 2
        for s in p["situations"]:
            assert s.get("id") and s.get("text") and len(s["options"]) >= 2
            assert sum(1 for o in s["options"] if o["outcome"] == "good") == 1
            for o in s["options"]:
                assert o.get("text") and o.get("feedback") and o["outcome"] in ("good", "risky", "bad")


@pytest.mark.django_db
def test_apply_it_check_tasks_are_well_formed(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.exists()
    for task in checks:
        opts = task.payload.get("options", [])
        assert len(opts) == 4 and sum(1 for o in opts if o["correct"]) == 1
        assert task.payload.get("question") and task.payload.get("hint", "").strip()
        for o in opts:
            assert o["explanation"].strip()


# --------------------------------------------------------------------------
# Coverage, visuals, quiz, voice, idempotency
# --------------------------------------------------------------------------


def _all_strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _all_strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _all_strings(v)]
    return []


@pytest.mark.django_db
def test_module_one_simulation_is_screen_driven(seeded):
    """The rebuilt simulation is scene-based, and every decision scene shows a
    realistic device-framed screen the learner reads to decide."""
    sim = seeded.simulation.decision_points
    assert sim["kind"] == "scenes"
    decisions = [s for s in sim["scenes"].values() if s.get("choices")]
    assert len(decisions) >= 2
    for sc in decisions:
        screen = sc.get("screen")
        assert screen, "each decision scene must carry a device-framed screen"
        assert screen.get("chrome") in ("browser", "window", "phone")
        # something concrete to read: rows, an email, or a device list
        assert screen.get("rows") or screen.get("email") or screen.get("items")


@pytest.mark.django_db
def test_module_one_covers_the_required_ground(seeded):
    parts = [l.body_text for l in seeded.lessons.all()]
    for t in LessonTask.objects.filter(lesson__module=seeded):
        parts.append(t.body)
        parts.extend(_all_strings(t.payload))
    corpus = " ".join(parts).lower()
    # The CIA triad, what a network is, and the ACSC small-business baseline.
    assert "confidentiality" in corpus and "integrity" in corpus and "availability" in corpus
    assert "network" in corpus and "router" in corpus
    assert "multi-factor" in corpus or "wpa" in corpus or "guest network" in corpus
    assert "encrypt" in corpus and "https" in corpus


@pytest.mark.django_db
def test_module_one_uses_technical_diagrams_in_lesson_one(seeded):
    """Lesson 1's teaching panels carry professional TECHNICAL DIAGRAMS (own-origin
    inline-SVG partials, CSP-safe), not stock photos: a network topology, the data
    hops, the CIA triad and a labelled router. The one physical device photo
    (the router) is kept only as a supporting aid alongside its diagram. The
    comprehension CHECK reads a mockup router/Wi-Fi screen."""
    l1 = seeded.lessons.get(lesson_number=1)
    by_key = {t.task_key: t for t in l1.tasks.all()}
    diagrams = {
        "net-basics": "net-topology",
        "data-travels": "data-hops",
        "cia-triad": "cia-triad",
        "weak-points": "router-labelled",
        "who-is-on": "wifi-devices",
    }
    for key, dk in diagrams.items():
        assert by_key[key].diagram_key == dk, f"{key} should use diagram {dk}"
    # The generic filler photos are gone from the teaching panels.
    for key in ("net-basics", "data-travels", "cia-triad"):
        assert not (by_key[key].image or {}).get("src"), f"{key} should be diagram-only"
    # The router photo stays only as a supporting aid on weak-points.
    aid = by_key["weak-points"].image
    assert aid and aid.get("src") == "img/m1-router.webp"
    assert aid.get("caption") and aid.get("credit"), "the router aid keeps caption + credit"
    # No animations on any Lesson 1 panel (teaching lesson).
    for t in l1.tasks.all():
        assert (t.payload or {}).get("hero") not in ANIMATIONS


@pytest.mark.django_db
def test_module_one_lesson_one_visuals_are_own_origin(seeded, client):
    from django.contrib.auth import get_user_model

    user = get_user_model().objects.create_user(
        email="m1photo@example.com", password="x" * 14, is_verified=True
    )
    client.force_login(user)
    html = client.get(reverse("learn:lesson", args=[1, 1])).content.decode()
    # The teaching diagrams render as inline SVG figures (own-origin, CSP-safe).
    assert "cy-td__svg" in html and "<svg" in html
    # The router aid photo renders as an own-origin figure with a caption.
    assert "cy-photo__img" in html and "cy-photo__cap" in html
    assert "/static/img/m1-router.webp" in html or "img/m1-router.webp" in html
    # The retired filler photos are no longer on the page.
    for src in ("m1-network.webp", "m1-encryption.webp", "m1-records.webp"):
        assert src not in html, f"{src} should be gone from Lesson 1"


@pytest.mark.django_db
def test_module_one_quiz_is_exactly_ten_split_across_the_two_lessons(seeded):
    quiz = seeded.quiz
    assert quiz.pass_mark == 70
    assert quiz.questions.count() == 10
    per_lesson = Counter(quiz.questions.values_list("lesson_reference__lesson_number", flat=True))
    for n in (1, 2):
        assert per_lesson[n] >= 2, f"lesson {n} thin in the bank ({per_lesson[n]})"


@pytest.mark.django_db
def test_every_question_is_well_formed_for_the_engine_and_the_afe(seeded):
    lesson_ids = set(seeded.lessons.values_list("id", flat=True))
    for q in seeded.quiz.questions.select_related("lesson_reference"):
        answers = list(q.answers.all())
        assert len(answers) == 4 and sum(1 for a in answers if a.correct_answer) == 1
        for a in answers:
            assert a.explanation_text.strip()
        assert q.lesson_reference_id in lesson_ids


@pytest.mark.django_db
def test_lesson_and_quiz_voice_has_no_em_dashes(seeded):
    for task in LessonTask.objects.filter(lesson__module=seeded):
        blob = _content_blob(task)
        for d in DASHES:
            assert d not in blob, f"{task.task_key} contains a dash char {d!r}"
    for q in seeded.quiz.questions.all():
        blob = q.question_text + " " + " ".join(
            a.option_text + " " + a.explanation_text for a in q.answers.all()
        )
        for d in DASHES:
            assert d not in blob, f"quiz question {q.id} contains a dash char {d!r}"


@pytest.mark.django_db
def test_every_check_carries_a_hint(seeded):
    checks = LessonTask.objects.filter(lesson__module=seeded, kind="CHECK")
    assert checks.exists()
    for task in checks:
        assert task.payload.get("hint", "").strip(), f"{task.task_key} has no hint"


@pytest.mark.django_db
def test_the_seed_is_idempotent(seeded):
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
def test_reseeding_prunes_stale_quiz_options(seeded):
    q = seeded.quiz.questions.first()
    Answer.objects.create(question=q, option_text="STALE leftover option", correct_answer=True,
                          explanation_text="from an older version")
    assert q.answers.count() == 5
    call_command("seed_learning_content")
    q.refresh_from_db()
    assert q.answers.count() == 4 and q.answers.filter(correct_answer=True).count() == 1
