"""Forgot password (reset, not recovery).

Built entirely on Django's own PasswordResetView / PasswordResetConfirmView and
its token generator — no hand-rolled token logic here to get wrong. The tests
that matter most are the ones proving the *shape* of the feature: a stranger
probing the form learns nothing about who has an account, and a link is good
for exactly one password change.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse

User = get_user_model()

PASSWORD = "correct-horse-battery"
NEW_PASSWORD = "new-correct-horse-battery"


@pytest.fixture
def student(db):
    return User.objects.create_user(
        email="meredith@example.com",
        password=PASSWORD,
        first_name="Meredith",
        last_name="Nguyen",
        role=User.Role.STUDENT,
        is_verified=True,
    )


def request_reset(client, email="meredith@example.com"):
    return client.post(reverse("authentication:password_reset"), {"email": email})


def extract_reset_url(body):
    """Pull the confirm link out of the emailed body."""
    match = re.search(r"https?://\S+/reset/\S+/\S+/", body)
    assert match, f"no reset link found in the email:\n{body}"
    return match.group(0)


# --------------------------------------------------------------------------
# The request form
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_reset_request_page_renders(client):
    assert client.get(reverse("authentication:password_reset")).status_code == 200


@pytest.mark.django_db
def test_login_page_links_to_reset(client):
    # /login/ with no ?as= is the role chooser, not the form itself.
    response = client.get(reverse("authentication:login") + "?as=student")
    assert reverse("authentication:password_reset").encode() in response.content
    assert b"Forgot your password?" in response.content


# --------------------------------------------------------------------------
# The end-to-end flow
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_reset_flow_end_to_end(client, student):
    response = request_reset(client)
    assert response.status_code == 302
    assert response.url == reverse("authentication:password_reset_done")
    assert len(mail.outbox) == 1

    reset_url = extract_reset_url(mail.outbox[0].body)

    # Following the emailed link swaps the real token in the URL for a
    # one-time session placeholder (Django's own behaviour) so it never sits
    # in a Referer header on the confirm page.
    confirm_response = client.get(reset_url, follow=True)
    assert confirm_response.status_code == 200
    assert confirm_response.context["validlink"] is True

    set_password_url = confirm_response.redirect_chain[-1][0]
    response = client.post(
        set_password_url,
        {"new_password1": NEW_PASSWORD, "new_password2": NEW_PASSWORD},
    )
    assert response.status_code == 302
    assert response.url == reverse("authentication:password_reset_complete")

    assert client.login(username=student.email, password=NEW_PASSWORD)
    client.logout()
    assert not client.login(username=student.email, password=PASSWORD)


@pytest.mark.django_db
def test_reset_email_is_plain_language_and_carries_no_template_leaks(client, student):
    request_reset(client)
    body = mail.outbox[0].body
    subject = mail.outbox[0].subject

    for token in ("{{", "}}", "{%", "%}"):
        assert token not in body
        assert token not in subject

    assert student.first_name in body


# --------------------------------------------------------------------------
# Not revealing whether an email is registered
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_unknown_email_produces_identical_response(client, student):
    known_response = client.post(
        reverse("authentication:password_reset"),
        {"email": "meredith@example.com"},
        follow=True,
    )
    unknown_response = client.post(
        reverse("authentication:password_reset"),
        {"email": "nobody-here@example.com"},
        follow=True,
    )

    assert known_response.status_code == unknown_response.status_code == 200
    assert known_response.redirect_chain == unknown_response.redirect_chain
    assert known_response.content == unknown_response.content

    # The pages are identical; only the mail actually sent differs.
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_unregistered_email_still_redirects_to_done(client):
    response = request_reset(client, email="nobody-here@example.com")
    assert response.status_code == 302
    assert response.url == reverse("authentication:password_reset_done")
    assert len(mail.outbox) == 0


# --------------------------------------------------------------------------
# Token lifecycle: single-use and time-limited
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_used_token_cannot_be_reused(client, student):
    request_reset(client)
    reset_url = extract_reset_url(mail.outbox[0].body)

    confirm_response = client.get(reset_url, follow=True)
    set_password_url = confirm_response.redirect_chain[-1][0]
    client.post(
        set_password_url,
        {"new_password1": NEW_PASSWORD, "new_password2": NEW_PASSWORD},
    )

    # Click the *same* emailed link again — a fresh browser session, exactly
    # as if the user (or someone who found the email) opened it a second
    # time. The token was generated from the old password hash, so it no
    # longer matches once the password has changed.
    second_client = client.__class__()
    replay_response = second_client.get(reset_url, follow=True)
    assert replay_response.status_code == 200
    assert replay_response.context["validlink"] is False
    assert b"That link didn" in replay_response.content


@pytest.mark.django_db
def test_expired_token_is_rejected(client, student):
    request_reset(client)
    reset_url = extract_reset_url(mail.outbox[0].body)

    # A negative timeout means "already older than the window" for every
    # token, regardless of when it was actually issued — the same trick the
    # email-verification expiry test uses for its own token.
    with override_settings(PASSWORD_RESET_TIMEOUT=-1):
        response = client.get(reset_url, follow=True)

    assert response.status_code == 200
    assert response.context["validlink"] is False
    assert b"That link didn" in response.content


# --------------------------------------------------------------------------
# Rate limiting (so the form can't be used to spam a stranger's inbox)
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_repeated_reset_requests_are_rate_limited(client, student, rate_limiting):
    for _ in range(5):
        request_reset(client)

    response = request_reset(client)

    assert response.status_code == 429
    assert b"slow down" in response.content.lower()


@pytest.mark.django_db
def test_rate_limit_respects_ratelimit_enable_setting(client, student, settings):
    """RATELIMIT_ENABLE off (the default under test) means the limit never fires."""
    settings.RATELIMIT_ENABLE = False

    for _ in range(10):
        response = request_reset(client)

    assert response.status_code == 302
