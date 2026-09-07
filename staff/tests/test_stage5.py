"""Stage 5 — content: preview a lesson as a student, and the authored-vs-edited
distinction. The preview reaches past the sequential lock, writes nothing, and
is administrator-only.
"""

import pytest
from django.urls import reverse

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord

PASSWORD = "correct-horse-battery"


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)
    # Two modules; module 2 sits behind module 1's sequential lock.
    m1 = Module.objects.create(title="Module 1", order_index=1,
                               is_published=True, created_by=admin)
    Lesson.objects.create(module=m1, lesson_number=1, title="Intro lesson")
    m2 = Module.objects.create(title="Module 2", order_index=2,
                               is_published=True, created_by=admin)
    locked_lesson = Lesson.objects.create(module=m2, lesson_number=1, title="Locked lesson")
    return {"admin": admin, "m1": m1, "m2": m2, "locked_lesson": locked_lesson,
            "first_lesson": m1.lessons.first()}


def test_preview_renders_the_room_with_a_banner(client, world):
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:lesson_preview", args=[world["first_lesson"].pk]))
    assert resp.status_code == 200
    body = resp.content.decode()
    assert "cy-previewbar" in body
    assert "Intro lesson" in body
    assert "as a student would" in body


def test_preview_bypasses_the_sequential_lock(client, world):
    """An admin who has not completed module 1 can still preview module 2's
    lesson — the student view would 403 here."""
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:lesson_preview", args=[world["locked_lesson"].pk]))
    assert resp.status_code == 200
    assert "Locked lesson" in resp.content.decode()


def test_preview_writes_nothing(client, world):
    client.force_login(world["admin"])
    client.get(reverse("staff:lesson_preview", args=[world["first_lesson"].pk]))
    assert ProgressRecord.objects.filter(user=world["admin"]).count() == 0


def test_edit_page_shows_authored_or_edited_source(client, world):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:lesson_edit", args=[world["first_lesson"].pk])).content.decode()
    assert "Authored in code" in body        # not yet edited in console
    assert "Preview as student" in body


def test_preview_is_admin_only(client, world):
    student = User.objects.create_user(
        email="s@example.com", password=PASSWORD, first_name="S", last_name="T",
        role=User.Role.STUDENT, is_verified=True,
    )
    UserProfile.objects.create(user=student)
    client.force_login(student)
    assert client.get(reverse("staff:lesson_preview", args=[world["first_lesson"].pk])).status_code == 403


def test_preview_sends_anonymous_to_login(client, world):
    resp = client.get(reverse("staff:lesson_preview", args=[world["first_lesson"].pk]))
    assert resp.status_code == 302
    assert reverse("authentication:login") in resp.url
