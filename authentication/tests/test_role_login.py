"""Role-first login: the chooser, the framed form, and the demo accounts.

The design: the login page leads with two prominent "Log in as Student /
Administrator" buttons. Each opens the SAME secure email + password + 2FA form,
framed for that role. The framing is cosmetic — the role a user actually gets
is read from their account, never from the button. The security tests below pin
exactly that: there is no way to grant yourself a role from the login page.
"""

import re

import pytest
from django.core import mail
from django.core.management import call_command
from django.urls import reverse

from authentication.demo import DEMO_ACCOUNTS
from authentication.models import User, UserProfile

PASSWORD = "correct-horse-battery"


@pytest.fixture
def seeded(db):
    call_command("seed_demo_accounts")


# --- The chooser (primary way in) ------------------------------------------


def test_login_root_shows_the_two_role_buttons(client, db):
    resp = client.get(reverse("authentication:login"))
    body = resp.content.decode()
    assert resp.status_code == 200
    assert "Log in as Student" in body
    assert "Log in as Administrator" in body
    # Each button leads to the framed form, not to a role it grants.
    assert "?as=student" in body
    assert "?as=admin" in body
    # The chooser is not the password form.
    assert 'name="password"' not in body


def test_login_page_has_no_role_selector(client, db):
    """Anti-escalation: no free-text or <select> role input anywhere."""
    for url in (
        reverse("authentication:login"),
        reverse("authentication:login") + "?as=admin",
    ):
        body = client.get(url).content.decode().lower()
        assert "<select" not in body
        assert 'name="role"' not in body


# --- The framed form -------------------------------------------------------


@pytest.mark.parametrize(
    "key,heading",
    [("student", "Student sign-in"), ("admin", "Administrator sign-in")],
)
def test_as_param_frames_the_form(client, db, key, heading):
    resp = client.get(reverse("authentication:login") + f"?as={key}")
    body = resp.content.decode()
    assert resp.status_code == 200
    assert heading in body
    # It IS the real login form, framed — password field present.
    assert 'name="password"' in body
    # The framing rides along a failed submit.
    assert f'name="as" value="{key}"' in body


def test_unknown_as_falls_back_to_the_chooser(client, db):
    """A hand-typed ?as= is not trusted — it shows the chooser, not a form."""
    resp = client.get(reverse("authentication:login") + "?as=superuser")
    body = resp.content.decode()
    assert "Log in as Student" in body
    assert 'name="password"' not in body


# --- Framing never grants a role (the whole security point) ----------------


def test_framing_does_not_change_who_you_authenticate_as(client, seeded):
    """Signing in through the 'Administrator' frame with a Student's password
    starts the Student's login — the frame is ignored by authentication."""
    student = User.objects.get(email=DEMO_ACCOUNTS["student"]["email"])

    resp = client.post(
        reverse("authentication:login"),
        {
            "username": student.email,
            "password": DEMO_ACCOUNTS["student"]["password"],
            "as": "admin",  # wrong frame on purpose
            "next": "",
        },
    )

    # Password ok → straight to the 2FA code step (no session yet), for the
    # Student, regardless of the "admin" frame.
    assert resp.status_code == 302
    assert resp.url == reverse("authentication:login_code")
    assert client.session["pending_2fa_user_id"] == student.pk
    assert "_auth_user_id" not in client.session  # not logged in until the code
    assert len(mail.outbox) == 1  # the code went to the Student's address
    assert student.email in mail.outbox[0].to


def test_bad_password_rerenders_the_framed_form(client, seeded):
    resp = client.post(
        reverse("authentication:login"),
        {"username": DEMO_ACCOUNTS["admin"]["email"], "password": "wrong", "as": "admin"},
    )
    body = resp.content.decode()
    assert resp.status_code == 200
    # Still framed as admin, still no session.
    assert "Administrator sign-in" in body
    assert "_auth_user_id" not in client.session


# --- The demo accounts (credentials the supervisor types) ------------------


def test_seed_creates_both_accounts_with_the_right_roles_and_flags(seeded):
    admin = User.objects.get(email=DEMO_ACCOUNTS["admin"]["email"])
    student = User.objects.get(email=DEMO_ACCOUNTS["student"]["email"])

    assert admin.role == User.Role.ADMINISTRATOR
    assert admin.is_staff and admin.is_superuser
    assert student.role == User.Role.STUDENT
    assert not student.is_staff and not student.is_superuser

    for user in (admin, student):
        assert user.is_active and user.is_verified
        assert UserProfile.objects.filter(user=user).exists()

    assert admin.check_password(DEMO_ACCOUNTS["admin"]["password"])
    assert student.check_password(DEMO_ACCOUNTS["student"]["password"])


def test_seed_is_idempotent_and_resets_state(seeded):
    admin = User.objects.get(email=DEMO_ACCOUNTS["admin"]["email"])
    admin.is_active = False
    admin.set_password("tampered")
    admin.save()

    call_command("seed_demo_accounts")

    assert User.objects.filter(email=DEMO_ACCOUNTS["admin"]["email"]).count() == 1
    admin.refresh_from_db()
    assert admin.is_active
    assert admin.check_password(DEMO_ACCOUNTS["admin"]["password"])
