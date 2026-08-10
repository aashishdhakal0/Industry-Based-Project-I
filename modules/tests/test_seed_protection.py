"""The seed must never silently wipe an admin's console edit.

`seed_learning_content` refreshes content from the authored Python files. A row
an admin has edited (admin_edited=True) is left untouched by a routine reseed and
only reset by an explicit --force. Publish state (is_published / is_active) is
set only on create, so a publish/unpublish decision also survives a reseed.

These run the real seed (as the suite does elsewhere), so they exercise the
actual command, not a stand-in.
"""

import pytest
from django.core.management import call_command

from authentication.models import User
from modules.models import Lesson, Module
from quizzes.models import Question


@pytest.fixture
def seeded(db):
    # The seed needs a user to own the content.
    User.objects.create_user(
        email="root@example.com", password="x", role=User.Role.ADMINISTRATOR,
    )
    call_command("seed_learning_content")


def _first_lesson():
    return Lesson.objects.filter(module__order_index=1).order_by("lesson_number").first()


# --- Admin edits survive a routine reseed ----------------------------------

def test_reseed_preserves_an_admin_edited_module(seeded):
    module = Module.objects.get(order_index=1)
    module.title = "Admin's module title"
    module.description = "Admin rewrote this."
    module.admin_edited = True
    module.save()

    call_command("seed_learning_content")

    module.refresh_from_db()
    assert module.admin_edited is True
    assert module.title == "Admin's module title"
    assert module.description == "Admin rewrote this."


def test_reseed_preserves_an_admin_edited_lesson(seeded):
    lesson = _first_lesson()
    lesson.title = "Admin's lesson title"
    lesson.body_text = "<p>Admin rewrote the body.</p>"
    lesson.admin_edited = True
    lesson.save()

    call_command("seed_learning_content")

    lesson.refresh_from_db()
    assert lesson.admin_edited is True
    assert lesson.title == "Admin's lesson title"
    assert "Admin rewrote the body." in lesson.body_text


def test_reseed_preserves_an_admin_edited_question(seeded):
    question = Question.objects.filter(quiz__module__order_index=1).order_by("ordering").first()
    question.question_text = "An admin's question?"
    question.admin_edited = True
    question.save()
    answer = question.answers.first()
    answer.explanation_text = "An admin's explanation."
    answer.save()

    call_command("seed_learning_content")

    question.refresh_from_db()
    answer.refresh_from_db()
    assert question.admin_edited is True
    assert question.question_text == "An admin's question?"
    assert answer.explanation_text == "An admin's explanation."


# --- Unedited content still tracks the authored source ---------------------

def test_reseed_refreshes_content_that_was_not_admin_edited(seeded):
    """A row without the lock is still reasserted from the Python source, so a
    content author's edits keep flowing on a normal reseed."""
    lesson = _first_lesson()
    authored_title = lesson.title
    lesson.title = "Drifted, but not locked"
    lesson.save()                       # admin_edited stays False

    call_command("seed_learning_content")

    lesson.refresh_from_db()
    assert lesson.title == authored_title


# --- Publish decisions survive a reseed ------------------------------------

def test_reseed_preserves_publish_state(seeded):
    """is_published / is_active are set only on create, so an admin's publish or
    unpublish is not undone by a reseed even without the content lock."""
    lesson = _first_lesson()
    lesson.is_active = False
    lesson.save()
    module = Module.objects.get(order_index=2)
    module.is_published = False
    module.save()

    call_command("seed_learning_content")

    lesson.refresh_from_db()
    module.refresh_from_db()
    assert lesson.is_active is False
    assert module.is_published is False


# --- --force is the deliberate reset ---------------------------------------

def test_force_reseed_reverts_admin_edits_and_clears_the_flag(seeded):
    lesson = _first_lesson()
    authored_title = lesson.title
    lesson.title = "Admin's title"
    lesson.body_text = "<p>Admin body.</p>"
    lesson.admin_edited = True
    lesson.save()

    call_command("seed_learning_content", "--force")

    lesson.refresh_from_db()
    assert lesson.admin_edited is False
    assert lesson.title == authored_title
    assert "Admin body." not in lesson.body_text
