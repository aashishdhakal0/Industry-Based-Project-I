"""Editing module content from the console.

Covers the module/lesson/question edit views: access control (a real 403 for
non-admins), that each edit saves and is written to the audit log, that lesson
HTML is sanitised on save (no stored XSS), and that the quiz-question editor
enforces its two invariants (exactly one correct, non-empty explanations).
"""

import pytest
from django.urls import reverse

from authentication.models import User, UserProfile
from modules.models import Lesson, Module
from quizzes.models import Answer, Question, Quiz
from staff.models import AdminAction

PASSWORD = "correct-horse-battery"


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)

    student = User.objects.create_user(
        email="stu@example.com", password=PASSWORD, first_name="Sam",
        role=User.Role.STUDENT, is_verified=True,
    )
    UserProfile.objects.create(user=student)

    module = Module.objects.create(
        title="Network Security", description="Old description", order_index=1,
        is_published=True, created_by=admin,
    )
    lesson = Lesson.objects.create(
        module=module, lesson_number=1, title="What a network is",
        body_text="<p>Intro.</p>", reading_time_minutes=5,
    )
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)
    question = Question.objects.create(
        quiz=quiz, question_text="What is a firewall?", lesson_reference=lesson,
    )
    answers = [
        Answer.objects.create(
            question=question, option_text=f"Option {c}",
            correct_answer=(c == "A"), explanation_text=f"Because {c}.",
        )
        for c in ("A", "B", "C", "D")
    ]

    return {"admin": admin, "student": student, "module": module,
            "lesson": lesson, "quiz": quiz, "question": question, "answers": answers}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Access control (a real 403, not a hidden link) ------------------------

@pytest.fixture
def edit_pages(world):
    return [
        reverse("staff:module_detail", args=[world["module"].order_index]),
        reverse("staff:quiz_view", args=[world["module"].order_index]),
        reverse("staff:lesson_edit", args=[world["lesson"].pk]),
        reverse("staff:question_edit", args=[world["question"].pk]),
    ]


def test_edit_pages_forbid_students(client, world, edit_pages):
    client.force_login(world["student"])
    for url in edit_pages:
        assert client.get(url).status_code == 403


def test_edit_pages_send_anonymous_to_login(client, world, edit_pages):
    for url in edit_pages:
        resp = client.get(url)
        assert resp.status_code == 302 and reverse("authentication:login") in resp.url


def test_lesson_publish_forbids_students(client, world):
    client.force_login(world["student"])
    resp = client.post(reverse("staff:lesson_publish", args=[world["lesson"].pk]))
    assert resp.status_code == 403


def test_admin_reaches_every_edit_page(client, world, edit_pages):
    as_admin(client, world)
    for url in edit_pages:
        assert client.get(url).status_code == 200


# --- Module edit -----------------------------------------------------------

def test_module_edit_saves_logs_and_locks(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:module_detail", args=[world["module"].order_index]),
        {"title": "Network Basics", "description": "A fresh description",
         "difficulty": Module.Difficulty.INTERMEDIATE, "duration_minutes": 45,
         "order_index": 1},
    )
    assert resp.status_code == 302
    world["module"].refresh_from_db()
    assert world["module"].title == "Network Basics"
    assert world["module"].description == "A fresh description"
    assert world["module"].difficulty == Module.Difficulty.INTERMEDIATE
    assert world["module"].duration_minutes == 45
    assert world["module"].admin_edited is True    # locked against a reseed
    assert AdminAction.objects.filter(action=AdminAction.Kind.EDIT_MODULE).exists()


def test_module_order_index_is_editable(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:module_detail", args=[world["module"].order_index]),
        {"title": "Network Security", "description": "d",
         "difficulty": Module.Difficulty.BEGINNER, "duration_minutes": 0,
         "order_index": 4},
    )
    assert resp.status_code == 302
    world["module"].refresh_from_db()
    assert world["module"].order_index == 4


def test_module_order_index_collision_is_rejected(client, world):
    """Moving onto another module's slot is a clean inline error, not a 500."""
    as_admin(client, world)
    other = Module.objects.create(
        title="Threats", order_index=2, is_published=True, created_by=world["admin"]
    )
    resp = client.post(
        reverse("staff:module_detail", args=[world["module"].order_index]),
        {"title": "Network Security", "description": "d",
         "difficulty": Module.Difficulty.BEGINNER, "duration_minutes": 0,
         "order_index": other.order_index},
    )
    assert resp.status_code == 200          # re-rendered with an error, not saved
    world["module"].refresh_from_db()
    assert world["module"].order_index == 1


# --- Lesson edit + sanitisation --------------------------------------------

def test_lesson_edit_saves_and_logs(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:lesson_edit", args=[world["lesson"].pk]),
        {"title": "Networks 101", "reading_time_minutes": 8,
         "body_text": "<p>Clean body.</p>"},
    )
    assert resp.status_code == 302
    world["lesson"].refresh_from_db()
    assert world["lesson"].title == "Networks 101"
    assert world["lesson"].reading_time_minutes == 8
    assert world["lesson"].admin_edited is True    # locked against a reseed
    assert AdminAction.objects.filter(action=AdminAction.Kind.EDIT_LESSON).exists()


def test_lesson_edit_sanitises_body_html(client, world):
    """A security platform must never store XSS from an edit."""
    as_admin(client, world)
    client.post(
        reverse("staff:lesson_edit", args=[world["lesson"].pk]),
        {"title": "X", "reading_time_minutes": 1,
         "body_text": '<p>ok</p><script>alert(1)</script>'
                      '<a href="javascript:alert(2)">bad</a>'},
    )
    world["lesson"].refresh_from_db()
    body = world["lesson"].body_text
    assert "<script>" not in body
    assert "javascript:" not in body
    assert "<p>ok</p>" in body


# --- Lesson publish toggle -------------------------------------------------

def test_lesson_publish_toggles_and_logs(client, world):
    as_admin(client, world)
    url = reverse("staff:lesson_publish", args=[world["lesson"].pk])

    client.post(url)
    world["lesson"].refresh_from_db()
    assert world["lesson"].is_active is False

    client.post(url)
    world["lesson"].refresh_from_db()
    assert world["lesson"].is_active is True
    assert AdminAction.objects.filter(action=AdminAction.Kind.UNPUBLISH_LESSON).exists()
    assert AdminAction.objects.filter(action=AdminAction.Kind.PUBLISH_LESSON).exists()


def test_lesson_publish_rejects_get(client, world):
    as_admin(client, world)
    assert client.get(reverse("staff:lesson_publish", args=[world["lesson"].pk])).status_code == 405


# --- Quiz view -------------------------------------------------------------

def test_quiz_view_shows_questions_and_marks_correct(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:quiz_view", args=[world["module"].order_index])).content.decode()
    assert "What is a firewall?" in body
    assert "Option A" in body
    assert "Because A." in body       # explanations are shown
    assert "is-correct" in body       # the correct option is marked


# --- Question edit + invariants --------------------------------------------

def _post_data(answers, correct_index, **overrides):
    data = {"question_text": "What is a firewall?", "correct": str(correct_index)}
    for i, _ in enumerate(answers):
        data[f"option_text_{i}"] = f"Option {chr(65 + i)}"
        data[f"explanation_{i}"] = f"Because {chr(65 + i)}."
    data.update(overrides)
    return data


def test_question_edit_saves_and_moves_the_correct_answer(client, world):
    as_admin(client, world)
    answers = world["answers"]
    resp = client.post(
        reverse("staff:question_edit", args=[world["question"].pk]),
        _post_data(answers, correct_index=2, question_text="Which one blocks traffic?",
                   explanation_2="C is the firewall."),
    )
    assert resp.status_code == 302
    world["question"].refresh_from_db()
    assert world["question"].question_text == "Which one blocks traffic?"

    fresh = {a.option_text: a for a in world["question"].answers.all()}
    # Exactly one correct, and it moved from A to C.
    correct = [a for a in fresh.values() if a.correct_answer]
    assert len(correct) == 1
    assert correct[0].option_text == "Option C"
    assert fresh["Option C"].explanation_text == "C is the firewall."
    assert world["question"].admin_edited is True    # locked against a reseed
    assert AdminAction.objects.filter(action=AdminAction.Kind.EDIT_QUESTION).exists()


def test_question_edit_requires_a_correct_answer(client, world):
    as_admin(client, world)
    data = _post_data(world["answers"], correct_index=0)
    data.pop("correct")            # nobody marked correct
    resp = client.post(reverse("staff:question_edit", args=[world["question"].pk]), data)
    assert resp.status_code == 200         # re-rendered with an error, not saved
    # The original correct answer (A) is untouched.
    world["answers"][0].refresh_from_db()
    assert world["answers"][0].correct_answer is True


def test_question_edit_requires_every_explanation(client, world):
    as_admin(client, world)
    data = _post_data(world["answers"], correct_index=1, explanation_1="")
    resp = client.post(reverse("staff:question_edit", args=[world["question"].pk]), data)
    assert resp.status_code == 200         # invalid, re-rendered
    # Nothing moved: A is still the correct answer.
    world["question"].refresh_from_db()
    correct = [a for a in world["question"].answers.all() if a.correct_answer]
    assert len(correct) == 1 and correct[0].option_text == "Option A"


# --- "Edited in console" badge ---------------------------------------------

def test_edited_badge_appears_once_a_lesson_is_edited(client, world):
    as_admin(client, world)
    detail = reverse("staff:module_detail", args=[world["module"].order_index])

    assert "Edited" not in client.get(detail).content.decode()
    client.post(
        reverse("staff:lesson_edit", args=[world["lesson"].pk]),
        {"title": "X", "reading_time_minutes": 1, "body_text": "<p>x</p>"},
    )
    assert "Edited" in client.get(detail).content.decode()


# --- Content health (overview card) ----------------------------------------

def test_content_health_counts_are_right(world):
    from staff import services

    world["lesson"].admin_edited = True
    world["lesson"].save()

    h = services.content_health()
    assert h["modules_total"] == 1
    assert h["modules_published"] == 1
    assert h["lessons_total"] == 1
    assert h["questions_total"] == 1
    assert h["edited_total"] == 1          # the one locked lesson


def test_overview_shows_the_content_card(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:overview")).content.decode()
    assert "Modules published" in body
    assert "Quiz questions" in body
