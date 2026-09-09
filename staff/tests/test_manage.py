"""Management console: access control, user actions (with guardrails), content.

Builds a small world with an admin, a module, and a few learners (one flagged,
one gone quiet) so the actions have something real to act on.
"""

from datetime import timedelta

import pytest
from django.core import mail
from django.urls import reverse
from django.utils import timezone

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult
from staff.models import AdminAction

PASSWORD = "correct-horse-battery"


def make_user(email, first, role=User.Role.STUDENT, **profile_kw):
    user = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Test",
        role=role, is_verified=True,
    )
    UserProfile.objects.create(user=user, **profile_kw)
    return user


@pytest.fixture
def env(db):
    admin = make_user("admin@example.com", "Ada", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])

    module = Module.objects.create(
        title="Network Security", order_index=1, is_published=True, created_by=admin
    )
    for n in (1, 2):
        Lesson.objects.create(module=module, lesson_number=n, title=f"L{n}")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)

    alice = make_user("alice@example.com", "Alice", points=110, last_active=timezone.now())
    for lesson in module.lessons.all():
        ProgressRecord.objects.create(user=alice, lesson=lesson)
    QuizResult.objects.create(user=alice, quiz=quiz, score=85, passed=True, attempt_number=1)

    flagged = make_user("flag@example.com", "Fred", flagged=True, flag_reason="behind")
    quiet = make_user(
        "quiet@example.com", "Quinn", points=10,
        last_active=timezone.now() - timedelta(days=20),
    )

    return {"admin": admin, "module": module, "quiz": quiz,
            "alice": alice, "flagged": flagged, "quiet": quiet}


def as_admin(client, env):
    client.force_login(env["admin"])
    return client


# --- Access control --------------------------------------------------------

GET_PAGES = ["staff:user_new", "staff:content"]
POST_ACTIONS = [
    "staff:change_role", "staff:toggle_active", "staff:resend_verification",
    "staff:nudge", "staff:toggle_flag",
]


def test_detail_and_pages_forbid_students(client, env):
    client.force_login(env["alice"])
    assert client.get(reverse("staff:learner_detail", args=[env["alice"].pk])).status_code == 403
    for name in GET_PAGES:
        assert client.get(reverse(name)).status_code == 403


def test_actions_forbid_students(client, env):
    client.force_login(env["alice"])
    for name in POST_ACTIONS:
        resp = client.post(reverse(name, args=[env["quiet"].pk]))
        assert resp.status_code == 403


def test_actions_send_anonymous_to_login(client, env):
    resp = client.post(reverse("staff:nudge", args=[env["alice"].pk]))
    assert resp.status_code == 302 and reverse("authentication:login") in resp.url


def test_get_on_a_post_action_is_405(client, env):
    as_admin(client, env)
    assert client.get(reverse("staff:nudge", args=[env["alice"].pk])).status_code == 405


# --- Learner detail --------------------------------------------------------

def test_learner_detail_renders_the_full_picture(client, env):
    as_admin(client, env)
    body = client.get(reverse("staff:learner_detail", args=[env["alice"].pk])).content.decode()
    assert "Alice" in body
    assert "Network Security" in body          # per-module progress
    assert "Quiz attempts" in body
    assert "85%" in body                        # the attempt
    assert "Manage account" in body             # the action panel


# --- Add user --------------------------------------------------------------

def test_add_user_creates_account_with_role(client, env):
    as_admin(client, env)
    resp = client.post(reverse("staff:user_new"), {
        "first_name": "Liam", "last_name": "Ng", "email": "liam@council.gov.au",
        "role": User.Role.INSTRUCTOR, "organisation": "Council",
        "password": "three-random-words-xyz",
    })
    liam = User.objects.get(email="liam@council.gov.au")
    assert liam.role == User.Role.INSTRUCTOR
    assert liam.is_active and liam.is_verified
    assert not liam.is_staff and not liam.is_superuser   # role != Django superuser
    assert UserProfile.objects.filter(user=liam).exists()
    assert liam.check_password("three-random-words-xyz")
    assert resp.status_code == 302
    assert AdminAction.objects.filter(action="add_user", target_user=liam).exists()


def test_add_user_rejects_duplicate_email(client, env):
    as_admin(client, env)
    resp = client.post(reverse("staff:user_new"), {
        "first_name": "Dupe", "last_name": "X", "email": "alice@example.com",
        "role": User.Role.STUDENT, "password": "three-random-words-xyz",
    })
    assert resp.status_code == 200
    assert b"already exists" in resp.content


def test_add_user_rejects_weak_password(client, env):
    as_admin(client, env)
    before = User.objects.count()
    resp = client.post(reverse("staff:user_new"), {
        "first_name": "Weak", "last_name": "X", "email": "weak@example.com",
        "role": User.Role.STUDENT, "password": "abc",
    })
    assert resp.status_code == 200
    assert User.objects.count() == before       # not created


# --- Change role + guardrails ----------------------------------------------

def test_change_role_updates_and_logs(client, env):
    as_admin(client, env)
    client.post(reverse("staff:change_role", args=[env["alice"].pk]),
                {"role": User.Role.INSTRUCTOR})
    env["alice"].refresh_from_db()
    assert env["alice"].role == User.Role.INSTRUCTOR
    assert AdminAction.objects.filter(action="role_change", target_user=env["alice"]).exists()


def test_cannot_change_your_own_role(client, env):
    as_admin(client, env)
    client.post(reverse("staff:change_role", args=[env["admin"].pk]),
                {"role": User.Role.STUDENT})
    env["admin"].refresh_from_db()
    assert env["admin"].role == User.Role.ADMINISTRATOR   # unchanged


def test_unknown_role_is_rejected(client, env):
    as_admin(client, env)
    resp = client.post(reverse("staff:change_role", args=[env["alice"].pk]),
                       {"role": "GOD_MODE"})
    assert resp.status_code == 403
    env["alice"].refresh_from_db()
    assert env["alice"].role == User.Role.STUDENT


def test_last_active_admin_helper():
    from staff.useractions import _is_last_active_admin
    # Pure logic: with a single active admin, they are the last one.
    from unittest.mock import patch
    admin = User(role=User.Role.ADMINISTRATOR, is_active=True, pk=1)
    with patch("staff.useractions._other_active_admin_exists", return_value=False):
        assert _is_last_active_admin(admin) is True
    with patch("staff.useractions._other_active_admin_exists", return_value=True):
        assert _is_last_active_admin(admin) is False


# --- Activate / deactivate -------------------------------------------------

def test_deactivate_and_reactivate(client, env):
    as_admin(client, env)
    client.post(reverse("staff:toggle_active", args=[env["alice"].pk]))
    env["alice"].refresh_from_db()
    assert env["alice"].is_active is False

    client.post(reverse("staff:toggle_active", args=[env["alice"].pk]))
    env["alice"].refresh_from_db()
    assert env["alice"].is_active is True
    assert AdminAction.objects.filter(target_user=env["alice"], action="deactivate").exists()
    assert AdminAction.objects.filter(target_user=env["alice"], action="activate").exists()


def test_cannot_deactivate_yourself(client, env):
    as_admin(client, env)
    client.post(reverse("staff:toggle_active", args=[env["admin"].pk]))
    env["admin"].refresh_from_db()
    assert env["admin"].is_active is True         # still standing


# --- Verification + nudge (emails) -----------------------------------------

def test_resend_verification_sends_mail(client, env):
    as_admin(client, env)
    client.post(reverse("staff:resend_verification", args=[env["alice"].pk]))
    assert len(mail.outbox) == 1
    assert env["alice"].email in mail.outbox[0].to


def test_nudge_sends_mail_and_logs(client, env):
    as_admin(client, env)
    client.post(reverse("staff:nudge", args=[env["quiet"].pk]))
    assert len(mail.outbox) == 1
    assert AdminAction.objects.filter(action="nudge", target_user=env["quiet"]).exists()


# --- Flag ------------------------------------------------------------------

def test_flag_and_unflag(client, env):
    as_admin(client, env)
    client.post(reverse("staff:toggle_flag", args=[env["alice"].pk]), {"reason": "no-show"})
    env["alice"].profile.refresh_from_db()
    assert env["alice"].profile.flagged is True
    assert env["alice"].profile.flag_reason == "no-show"

    client.post(reverse("staff:toggle_flag", args=[env["alice"].pk]))
    env["alice"].profile.refresh_from_db()
    assert env["alice"].profile.flagged is False


# --- Overview: attention + empty state -------------------------------------

def test_overview_surfaces_the_attention_cohorts(client, env):
    as_admin(client, env)
    body = client.get(reverse("staff:overview")).content.decode()
    # The four cohorts are consolidated into one "Needs attention" section.
    assert "Needs attention" in body
    assert "cy-c-attchip" in body            # the category-count chips
    assert "Fred" in body      # never started -> tagged Not started
    assert "Quinn" in body     # started then went quiet -> tagged with days quiet
    assert "days quiet" in body               # Quinn's stalled reason tag
    assert "stalled" in body                  # a category chip label


def test_overview_empty_state_when_no_learners(client, db):
    admin = make_user("solo@example.com", "Solo", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])
    client.force_login(admin)
    body = client.get(reverse("staff:overview")).content.decode()
    # Encouraging empty state, not a wall of zeros.
    assert "No learners yet" in body
    assert "cy-c-empty" in body


def test_overview_renders_gracefully_when_nobody_has_started(client, db):
    """Learners exist but none have progress: the dashboard still renders the
    completion hero (0%) and the activity chart degrades to an empty state rather
    than a flat line of zeros. No crash."""
    admin = make_user("q-admin@example.com", "Q", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])
    make_user("newbie1@example.com", "Newbie")   # no progress
    make_user("newbie2@example.com", "Other")    # no progress
    client.force_login(admin)
    resp = client.get(reverse("staff:overview"))
    assert resp.status_code == 200
    body = resp.content.decode()
    assert "cy-c-hero" in body                        # the completion hero
    assert "Training completion" in body
    assert "No learning activity" in body             # chart empty state, not zeros
    assert "cy-cal2__grid" not in body                # the old calendar is gone


def test_overview_uses_the_scoped_console_theme(client, env):
    as_admin(client, env)
    body = client.get(reverse("staff:overview")).content.decode()
    assert "cy-app--console" in body      # calm theme scoped on
    assert "admin.js" in body             # confirm/toast enhancements loaded


# --- Content management ----------------------------------------------------

def test_content_lists_modules_with_status(client, env):
    as_admin(client, env)
    body = client.get(reverse("staff:content")).content.decode()
    assert "Network Security" in body
    assert "Published" in body


def test_publish_toggle_unpublishes_and_logs(client, env):
    as_admin(client, env)
    client.post(reverse("staff:content_publish", args=[env["module"].order_index]))
    env["module"].refresh_from_db()
    assert env["module"].is_published is False
    assert AdminAction.objects.filter(action="unpublish").exists()
