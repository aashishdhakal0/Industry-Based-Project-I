"""Stage 2 — learner management depth: bulk actions, stored private notes,
certificate status, and audited resets.

Every state-changing path is checked for behaviour, the audit-log entry it must
write, and its access control (administrator-only, POST-only).
"""

import pytest
from django.core import mail
from django.urls import reverse

from authentication.models import Organisation, User, UserProfile
from certificates.models import Certificate
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult
from staff.models import AdminAction, LearnerNote

PASSWORD = "correct-horse-battery"


def mkadmin(email, first="Ada"):
    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Ops",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=u)
    return u


def mkstudent(email, first, verified=True):
    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Lee",
        role=User.Role.STUDENT, is_verified=verified,
    )
    UserProfile.objects.create(user=u)
    return u


@pytest.fixture
def world(db):
    admin = mkadmin("admin@example.com")
    module = Module.objects.create(title="Module 1", order_index=1,
                                   is_published=True, created_by=admin)
    for n in (1, 2):
        Lesson.objects.create(module=module, lesson_number=n, title=f"L{n}")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)

    alice = mkstudent("alice@example.com", "Alice")
    bob = mkstudent("bob@example.com", "Bob")
    return {"admin": admin, "module": module, "quiz": quiz,
            "alice": alice, "bob": bob}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Private notes -----------------------------------------------------------


def test_add_note_stores_and_audits(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:add_note", args=[world["alice"].pk]),
                       {"body": "Chased on 3 May, manager aware."})
    assert resp.status_code == 302
    note = LearnerNote.objects.get(learner=world["alice"])
    assert note.body == "Chased on 3 May, manager aware."
    assert note.author == world["admin"]
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.ADD_NOTE, target_user=world["alice"]
    ).exists()


def test_note_is_private_shown_on_detail_not_to_learner(client, world):
    as_admin(client, world)
    client.post(reverse("staff:add_note", args=[world["alice"].pk]),
               {"body": "Internal: on extended leave."})
    body = client.get(reverse("staff:learner_detail", args=[world["alice"].pk])).content.decode()
    assert "Internal: on extended leave." in body
    assert "Private notes" in body


def test_empty_note_is_rejected(client, world):
    as_admin(client, world)
    client.post(reverse("staff:add_note", args=[world["alice"].pk]), {"body": "  "})
    assert not LearnerNote.objects.filter(learner=world["alice"]).exists()


def test_add_note_is_admin_only_and_post_only(client, world):
    client.force_login(world["alice"])
    assert client.post(reverse("staff:add_note", args=[world["bob"].pk]), {"body": "x"}).status_code == 403
    as_admin(client, world)
    assert client.get(reverse("staff:add_note", args=[world["bob"].pk])).status_code == 405


# --- Certificate status ------------------------------------------------------


def test_certificate_status_shows_on_detail(client, world):
    Certificate.objects.create(user=world["alice"], grade="Distinction")
    as_admin(client, world)
    body = client.get(reverse("staff:learner_detail", args=[world["alice"].pk])).content.decode()
    assert "CYB-" in body
    assert "Distinction" in body
    assert "Valid" in body


def test_revoked_certificate_fails_public_verification(client, world):
    from django.utils import timezone
    cert = Certificate.objects.create(user=world["alice"], grade="Merit")
    cert.revoked_at = timezone.now()
    cert.save(update_fields=["revoked_at"])
    resp = client.get(reverse("certificates:verify", args=[cert.serial]))
    assert resp.status_code == 410
    assert "revoked" in resp.content.decode().lower()


# --- Resets (audited, cache reconciled) --------------------------------------


def _give_progress(world, learner):
    for lesson in world["module"].lessons.all():
        ProgressRecord.objects.create(user=learner, lesson=lesson)
    QuizResult.objects.create(user=learner, quiz=world["quiz"], score=50,
                              passed=False, attempt_number=1)
    QuizResult.objects.create(user=learner, quiz=world["quiz"], score=80,
                              passed=True, attempt_number=2)
    from modules.gamification import refresh_profile
    refresh_profile(learner)


def test_reset_quiz_clears_attempts_recomputes_and_audits(client, world):
    _give_progress(world, world["alice"])
    world["alice"].profile.refresh_from_db()
    points_before = world["alice"].profile.points
    assert points_before > 0

    as_admin(client, world)
    client.post(reverse("staff:reset", args=[world["alice"].pk]),
               {"module": world["module"].pk, "scope": "quiz"})

    assert QuizResult.objects.filter(user=world["alice"]).count() == 0
    # lessons remain
    assert ProgressRecord.objects.filter(user=world["alice"]).count() == 2
    world["alice"].profile.refresh_from_db()
    assert world["alice"].profile.points < points_before      # recomputed down
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.RESET_QUIZ, target_user=world["alice"]
    ).exists()


def test_reset_module_wipes_progress_and_audits(client, world):
    _give_progress(world, world["alice"])
    as_admin(client, world)
    client.post(reverse("staff:reset", args=[world["alice"].pk]),
               {"module": world["module"].pk, "scope": "module"})

    assert ProgressRecord.objects.filter(user=world["alice"]).count() == 0
    assert QuizResult.objects.filter(user=world["alice"]).count() == 0
    world["alice"].profile.refresh_from_db()
    assert world["alice"].profile.points == 0
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.RESET_PROGRESS, target_user=world["alice"]
    ).exists()


def test_reset_is_admin_only_and_post_only(client, world):
    client.force_login(world["alice"])
    assert client.post(reverse("staff:reset", args=[world["bob"].pk]),
                      {"module": world["module"].pk}).status_code == 403
    as_admin(client, world)
    assert client.get(reverse("staff:reset", args=[world["bob"].pk])).status_code == 405


# --- Password reset ----------------------------------------------------------


def test_send_password_reset_emails_and_audits(client, world):
    as_admin(client, world)
    client.post(reverse("staff:send_password_reset", args=[world["alice"].pk]))
    assert len(mail.outbox) == 1
    assert world["alice"].email in mail.outbox[0].to
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.PASSWORD_RESET, target_user=world["alice"]
    ).exists()


# --- Bulk actions ------------------------------------------------------------


def test_bulk_nudge_emails_all_and_audits_once(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:bulk_action"),
                      {"ids": [world["alice"].pk, world["bob"].pk], "action": "nudge"})
    assert resp.status_code == 302
    assert len(mail.outbox) == 2
    assert AdminAction.objects.filter(action=AdminAction.Kind.BULK_ACTION).count() == 1


def test_bulk_deactivate_skips_self_and_last_admin(client, world):
    # a second admin so the acting admin is not the last one
    other_admin = mkadmin("ben@example.com", "Ben")
    as_admin(client, world)
    client.post(reverse("staff:bulk_action"), {
        "ids": [world["alice"].pk, world["admin"].pk, other_admin.pk],
        "action": "deactivate",
    })
    world["alice"].refresh_from_db()
    world["admin"].refresh_from_db()
    other_admin.refresh_from_db()
    assert world["alice"].is_active is False        # student deactivated
    assert world["admin"].is_active is True         # acting admin skipped (self)
    assert other_admin.is_active is False           # a non-last admin can go


def test_bulk_deactivate_cannot_remove_the_last_admin(client, world):
    as_admin(client, world)  # world["admin"] is the only admin
    client.post(reverse("staff:bulk_action"),
               {"ids": [world["admin"].pk], "action": "deactivate"})
    world["admin"].refresh_from_db()
    assert world["admin"].is_active is True


def test_bulk_assign_org_sets_the_fk_and_mirror(client, world):
    org = Organisation.objects.create(name="Bendigo Council")
    as_admin(client, world)
    client.post(reverse("staff:bulk_action"), {
        "ids": [world["alice"].pk, world["bob"].pk],
        "action": "assign_org", "org": org.pk,
    })
    for s in (world["alice"], world["bob"]):
        s.profile.refresh_from_db()
        assert s.profile.org_id == org.pk
        assert s.profile.organisation == "Bendigo Council"


def test_bulk_export_returns_csv_of_selection(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:bulk_action"),
                      {"ids": [world["alice"].pk], "action": "export"})
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    text = resp.content.decode()
    assert "alice@example.com" in text
    assert "bob@example.com" not in text


def test_bulk_with_no_selection_is_handled(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:bulk_action"), {"ids": [], "action": "nudge"})
    assert resp.status_code == 302        # redirected back with an error message
    assert len(mail.outbox) == 0


def test_bulk_action_is_admin_only_and_post_only(client, world):
    client.force_login(world["alice"])
    assert client.post(reverse("staff:bulk_action"),
                      {"ids": [world["bob"].pk], "action": "nudge"}).status_code == 403
    as_admin(client, world)
    assert client.get(reverse("staff:bulk_action")).status_code == 405


def test_learners_list_renders_bulk_controls(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?view=list").content.decode()
    assert "data-bulk" in body
    assert 'name="ids"' in body
    assert "Export selection (CSV)" in body
