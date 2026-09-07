"""Stage 3 — bulk invite / workplace onboarding.

Parsing and classification, the preview (no writes), the audited batch create
with role + organisation, least-privilege guarantees, CSV upload, and access
control.
"""

import pytest
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from authentication.models import Organisation, User, UserProfile
from staff import services
from staff.models import AdminAction

PASSWORD = "correct-horse-battery"


@pytest.fixture
def admin(db):
    u = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        last_name="Ops", role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=u)
    return u


# --- Parsing + classification ------------------------------------------------


def test_parse_emails_is_forgiving():
    got = services.parse_emails("a@x.com\nb@x.com, c@x.com; D@X.COM\nName <e@x.com>")
    assert got == ["a@x.com", "b@x.com", "c@x.com", "d@x.com", "e@x.com"]


def test_classify_splits_new_existing_invalid(admin):
    User.objects.create_user(email="taken@x.com", password=PASSWORD,
                             first_name="T", last_name="K", role=User.Role.STUDENT)
    result = services.classify_invites(
        ["new@x.com", "new@x.com", "taken@x.com", "bad-email", "TAKEN@x.com"]
    )
    assert result["new"] == ["new@x.com"]
    assert result["existing"] == ["taken@x.com"]      # de-duped, case-insensitive
    assert result["invalid"] == ["bad-email"]


# --- Preview (no writes) -----------------------------------------------------


def test_preview_creates_nothing(client, admin):
    client.force_login(admin)
    before = User.objects.count()
    resp = client.post(reverse("staff:bulk_invite"),
                      {"emails": "one@x.com\ntwo@x.com", "role": "STUDENT"})
    assert resp.status_code == 200
    assert "to create" in resp.content.decode()
    assert User.objects.count() == before        # nothing written on preview
    assert not AdminAction.objects.filter(action=AdminAction.Kind.BULK_INVITE).exists()


# --- Batch create ------------------------------------------------------------


def test_create_makes_accounts_with_role_and_org_and_audits(client, admin):
    org = Organisation.objects.create(name="Wattle Grove Medical Centre")
    client.force_login(admin)
    resp = client.post(reverse("staff:bulk_invite"), {
        "action": "create",
        "emails": "steph@wg.com.au\ndilan@wg.com.au",
        "role": "STUDENT", "org": org.pk, "send_invite": "on",
    })
    assert resp.status_code == 302
    steph = User.objects.get(email="steph@wg.com.au")
    assert steph.role == User.Role.STUDENT
    assert steph.is_active and steph.is_verified
    assert steph.profile.org_id == org.pk
    assert steph.profile.organisation == "Wattle Grove Medical Centre"
    assert User.objects.filter(email="dilan@wg.com.au").exists()
    # each was emailed a set-password link
    assert len(mail.outbox) == 2
    action = AdminAction.objects.get(action=AdminAction.Kind.BULK_INVITE)
    assert "2" in action.summary


def test_create_never_grants_django_staff_or_superuser(client, admin):
    """Least privilege: even inviting Administrators grants the console role only."""
    client.force_login(admin)
    client.post(reverse("staff:bulk_invite"), {
        "action": "create", "emails": "newadmin@x.com", "role": "ADMINISTRATOR",
    })
    u = User.objects.get(email="newadmin@x.com")
    assert u.role == User.Role.ADMINISTRATOR
    assert u.is_staff is False
    assert u.is_superuser is False


def test_create_skips_duplicates_and_invalid(client, admin):
    User.objects.create_user(email="dup@x.com", password=PASSWORD,
                             first_name="D", last_name="U", role=User.Role.STUDENT)
    client.force_login(admin)
    before = User.objects.count()
    client.post(reverse("staff:bulk_invite"), {
        "action": "create",
        "emails": "fresh@x.com\ndup@x.com\nnot-valid",
        "role": "STUDENT",
    })
    assert User.objects.count() == before + 1     # only fresh@x.com
    assert User.objects.filter(email="fresh@x.com").exists()


def test_create_without_send_invite_emails_nobody(client, admin):
    client.force_login(admin)
    client.post(reverse("staff:bulk_invite"), {
        "action": "create", "emails": "quiet@x.com", "role": "STUDENT",
    })
    assert User.objects.filter(email="quiet@x.com").exists()
    assert len(mail.outbox) == 0


def test_csv_upload_is_parsed(client, admin):
    client.force_login(admin)
    csv = SimpleUploadedFile(
        "staff.csv",
        b"name,email\nAlice,alice@csv.com\nBob,bob@csv.com\n",
        content_type="text/csv",
    )
    resp = client.post(reverse("staff:bulk_invite"),
                      {"emails": "", "role": "STUDENT", "csv": csv})
    body = resp.content.decode()
    assert "alice@csv.com" in body and "bob@csv.com" in body


# --- Access control ----------------------------------------------------------


def test_invite_is_admin_only(client, admin):
    student = User.objects.create_user(
        email="s@x.com", password=PASSWORD, first_name="S", last_name="T",
        role=User.Role.STUDENT, is_verified=True,
    )
    client.force_login(student)
    assert client.get(reverse("staff:bulk_invite")).status_code == 403
    assert client.post(reverse("staff:bulk_invite"),
                      {"action": "create", "emails": "x@x.com"}).status_code == 403


def test_invite_sends_anonymous_to_login(client, admin):
    resp = client.get(reverse("staff:bulk_invite"))
    assert resp.status_code == 302
    assert reverse("authentication:login") in resp.url
