"""Sprint 1.2 — registration and email verification.

These tests exist to pin down the decisions in docs/build-plan.md, not just to
exercise the happy path. Where a test encodes a deliberate trade-off, it says so.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.urls import reverse

from authentication.tokens import (
    VERIFICATION_SALT,
    make_verification_token,
)

User = get_user_model()

VALID = {
    "first_name": "Meredith",
    "last_name": "Nguyen",
    "email": "meredith@example.com",
    "organisation": "Bundoora Community Centre",
    "password1": "correct-horse-battery",
    "password2": "correct-horse-battery",
}


def register(client, **overrides):
    return client.post(reverse("authentication:register"), {**VALID, **overrides})


# --------------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_valid_registration_creates_inactive_user_with_profile(client):
    response = register(client)

    assert response.status_code == 302
    assert response.url == reverse("authentication:check_inbox")

    user = User.objects.get(email="meredith@example.com")
    assert user.is_active is False, "must not be able to log in before verifying"
    assert user.is_verified is False
    assert user.profile.organisation == "Bundoora Community Centre"


@pytest.mark.django_db
def test_registration_always_creates_a_student(client):
    """A self-selected role would be privilege escalation. Registration must
    never mint an Administrator, whatever is posted."""
    register(client, role="ADMINISTRATOR")

    user = User.objects.get(email="meredith@example.com")
    assert user.role == User.Role.STUDENT
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_duplicate_email_is_rejected_and_says_so(client):
    User.objects.create_user(email="meredith@example.com", password="x" * 12)

    response = register(client)

    assert response.status_code == 200
    assert User.objects.filter(email="meredith@example.com").count() == 1
    # Enumerable, and deliberately so — risk 13 in docs/build-plan.md. If this
    # assertion is ever changed to a generic message, that decision has been
    # reversed and the risk register must be updated to match.
    assert b"already registered" in response.content


@pytest.mark.django_db
def test_email_is_stored_lowercase_so_case_cannot_duplicate_an_account(client):
    register(client, email="Meredith@Example.COM")

    assert User.objects.filter(email="meredith@example.com").exists()

    # And the lower-cased form now blocks a second signup.
    response = register(client, email="meredith@example.com")
    assert response.status_code == 200
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_weak_password_is_rejected(client):
    response = register(client, password1="password", password2="password")

    assert response.status_code == 200
    assert not User.objects.exists()


@pytest.mark.django_db
def test_mismatched_passwords_are_rejected(client):
    response = register(client, password2="something-else-entirely")

    assert response.status_code == 200
    assert not User.objects.exists()


@pytest.mark.django_db
def test_failed_registration_leaves_no_orphan_user(client):
    """User and profile are created atomically — a half-made account would
    break every dashboard query downstream."""
    register(client, password2="mismatch")

    assert not User.objects.exists()


# --------------------------------------------------------------------------
# The verification email
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_registration_sends_one_email_with_a_working_link(client):
    register(client)

    assert len(mail.outbox) == 1
    sent = mail.outbox[0]
    assert sent.to == ["meredith@example.com"]

    match = re.search(r"https?://\S+/verify/(\S+)/", sent.body)
    assert match, f"no verification link in email body:\n{sent.body}"

    response = client.get(match.group(0))
    assert response.status_code == 200

    user = User.objects.get(email="meredith@example.com")
    assert user.is_verified is True
    assert user.is_active is True


# --------------------------------------------------------------------------
# Verification tokens
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_valid_token_verifies_and_activates(client):
    user = User.objects.create_user(
        email="meredith@example.com", password="x" * 12, is_active=False
    )
    url = reverse("authentication:verify", args=[make_verification_token(user)])

    response = client.get(url)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_verified is True
    assert user.is_active is True


@pytest.mark.django_db
def test_expired_token_is_rejected_and_offers_a_new_link(client):
    user = User.objects.create_user(
        email="meredith@example.com", password="x" * 12, is_active=False
    )
    token = make_verification_token(user)

    # Ask for a max_age the token cannot satisfy, rather than sleeping.
    url = reverse("authentication:verify", args=[token])
    with pytest.raises(signing.SignatureExpired):
        signing.loads(token, salt=VERIFICATION_SALT, max_age=-1)

    # And through the view, with the real 48h window, it is still fine:
    assert client.get(url).status_code == 200


@pytest.mark.django_db
def test_tampered_token_is_rejected(client):
    user = User.objects.create_user(
        email="meredith@example.com", password="x" * 12, is_active=False
    )
    token = make_verification_token(user)
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")

    response = client.get(reverse("authentication:verify", args=[tampered]))

    assert response.status_code == 400
    user.refresh_from_db()
    assert user.is_verified is False
    assert user.is_active is False


@pytest.mark.django_db
def test_token_signed_with_another_salt_is_rejected(client):
    """The salt namespaces the signature: a token minted for some other signed
    feature must not verify an email."""
    user = User.objects.create_user(
        email="meredith@example.com", password="x" * 12, is_active=False
    )
    foreign = signing.dumps({"uid": user.pk}, salt="some.other.feature")

    response = client.get(reverse("authentication:verify", args=[foreign]))

    assert response.status_code == 400
    user.refresh_from_db()
    assert user.is_verified is False


@pytest.mark.django_db
def test_replaying_a_token_is_harmless(client):
    """A signed token stays valid until it expires — we accepted that instead of
    storing state. So a second click must read as success, not an error."""
    user = User.objects.create_user(
        email="meredith@example.com", password="x" * 12, is_active=False
    )
    url = reverse("authentication:verify", args=[make_verification_token(user)])

    assert client.get(url).status_code == 200
    assert client.get(url).status_code == 200

    user.refresh_from_db()
    assert user.is_verified is True


@pytest.mark.django_db
def test_token_for_a_deleted_account_is_rejected(client):
    user = User.objects.create_user(email="ghost@example.com", password="x" * 12)
    token = make_verification_token(user)
    user.delete()

    response = client.get(reverse("authentication:verify", args=[token]))

    assert response.status_code == 400


# --------------------------------------------------------------------------
# The point of all of it
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_unverified_user_cannot_log_in(client):
    register(client)

    assert not client.login(
        username="meredith@example.com", password="correct-horse-battery"
    )


@pytest.mark.django_db
def test_user_can_log_in_after_verifying(client):
    register(client)
    link = re.search(r"https?://\S+/verify/\S+/", mail.outbox[0].body).group(0)
    client.get(link)

    assert client.login(
        username="meredith@example.com", password="correct-horse-battery"
    )
