"""Sprint 1.3 — the emailed sign-in code.

Replaces the TOTP/authenticator-app flow. See the deviations table in
CLAUDE.md: the spec asks for an app, and we deviate on the method because our
users are non-technical adults. Every account gets a code — we deviate on how,
not on who.

The tests that matter most are the ones asserting what is NOT possible: a
password-only session reaching a page, a code being brute-forced, an expired
half-login finishing.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse

User = get_user_model()

PASSWORD = "correct-horse-battery"


def make_user(role=None, email="meredith@example.com", **extra):
    return User.objects.create_user(
        email=email,
        password=PASSWORD,
        first_name="Meredith",
        role=role or User.Role.STUDENT,
        is_verified=True,
        **extra,
    )


def login(client, user):
    return client.post(
        reverse("authentication:login"),
        {"username": user.email, "password": PASSWORD},
    )


def emailed_code():
    """Pull the code out of the most recent email."""
    match = re.search(r"^\s{4}(\d{6})\s*$", mail.outbox[-1].body, re.M)
    assert match, f"no 6-digit code in the email:\n{mail.outbox[-1].body}"
    return match.group(1)


def submit(client, code):
    return client.post(reverse("authentication:login_code"), {"code": code})


# --------------------------------------------------------------------------
# Coverage — every account, which is the point of the change
# --------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role", [User.Role.STUDENT, User.Role.INSTRUCTOR, User.Role.ADMINISTRATOR]
)
def test_every_role_is_sent_a_code(client, role):
    user = make_user(role, email=f"{role.lower()}@example.com")

    response = login(client, user)

    assert response.url == reverse("authentication:login_code")
    assert len(mail.outbox) == 1
    assert "_auth_user_id" not in client.session, "password alone is not a login"


@pytest.mark.django_db
def test_the_password_step_alone_cannot_reach_the_dashboard(client):
    """The half-authenticated window. If a pending login could reach a page,
    the second factor would be decorative."""
    login(client, make_user())

    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("authentication:login"))


# --------------------------------------------------------------------------
# The code
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_correct_code_completes_the_login(client):
    user = make_user()
    login(client, user)

    response = submit(client, emailed_code())

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert client.session.get("_auth_user_id") == str(user.pk)


@pytest.mark.django_db
def test_wrong_code_does_not_log_anyone_in(client):
    login(client, make_user())

    response = submit(client, "000000")

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_code_is_not_stored_in_the_session_in_plaintext(client):
    """Sessions get dumped into debug output and fixtures. Only the hash lives
    there, so a leaked session row doesn't hand over a live code."""
    login(client, make_user())
    code = emailed_code()

    assert code not in str(dict(client.session))


@pytest.mark.django_db
def test_a_code_cannot_be_reused(client):
    """Used once, gone. Otherwise a code glimpsed over a shoulder — or sitting
    in an inbox — stays live for its whole ten minutes."""
    user = make_user()
    login(client, user)
    code = emailed_code()

    submit(client, code)
    client.post(reverse("authentication:logout"))

    login(client, user)
    response = submit(client, code)

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_a_code_from_someone_elses_login_does_not_work(client):
    """The code is bound to the pending session, not floating in the ether."""
    make_user(email="a@example.com")
    other = make_user(email="b@example.com")

    login(client, other)
    other_code = emailed_code()

    client.post(reverse("authentication:logout"))
    login(client, User.objects.get(email="a@example.com"))

    response = submit(client, other_code)

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_codes_are_not_predictable(client):
    """`secrets`, not `random`. A Mersenne Twister seeded off the clock is
    predictable from its own output, which is fine for shuffling quiz questions
    and catastrophic for the thing guarding an account."""
    from authentication.utils import make_login_code

    codes = {make_login_code() for _ in range(400)}

    assert len(codes) > 350, "codes are colliding far more than chance allows"
    assert all(len(c) == 6 and c.isdigit() for c in codes)


# --------------------------------------------------------------------------
# Brute force — django-otp used to do this for us
# --------------------------------------------------------------------------


@pytest.mark.django_db
@override_settings(LOGIN_CODE_MAX_ATTEMPTS=5)
def test_the_code_dies_after_too_many_wrong_guesses(client):
    """Six digits is a million combinations, which sounds like plenty until you
    notice nothing stops someone with the password from simply trying.

    TOTPDevice carried django-otp's ThrottlingMixin and did this for us. It's
    gone, so we do it ourselves — this is exactly the protection that quietly
    disappears when a library is swapped out.
    """
    login(client, make_user())

    for _ in range(4):
        assert submit(client, "000000").status_code == 200

    response = submit(client, "000000")

    assert response.status_code == 403
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
@override_settings(LOGIN_CODE_MAX_ATTEMPTS=5)
def test_the_real_code_stops_working_once_attempts_are_exhausted(client):
    """Otherwise the cap protects nothing: guess four times, then land it."""
    login(client, make_user())
    code = emailed_code()

    for _ in range(5):
        submit(client, "000000")

    response = submit(client, code)

    assert "_auth_user_id" not in client.session
    assert response.status_code == 302
    assert response.url == reverse("authentication:login")


# --------------------------------------------------------------------------
# The pending window
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_code_page_without_a_pending_login_goes_back_to_login(client):
    response = client.get(reverse("authentication:login_code"))

    assert response.status_code == 302
    assert response.url == reverse("authentication:login")


@pytest.mark.django_db
def test_pending_login_expires(client):
    """A password typed and then abandoned shouldn't stay usable all day on a
    shared machine."""
    from datetime import timedelta

    from django.utils import timezone

    login(client, make_user())

    session = client.session
    session["pending_2fa_started_at"] = (
        timezone.now() - timedelta(minutes=11)
    ).isoformat()
    session.save()

    response = client.get(reverse("authentication:login_code"))

    assert response.url == reverse("authentication:login")


@pytest.mark.django_db
def test_an_account_deactivated_mid_login_cannot_finish(client):
    user = make_user()
    login(client, user)
    code = emailed_code()

    user.is_active = False
    user.save(update_fields=["is_active"])

    response = submit(client, code)

    assert response.status_code == 302
    assert response.url == reverse("authentication:login")
    assert "_auth_user_id" not in client.session


# --------------------------------------------------------------------------
# Resend
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_resend_issues_a_new_code_and_kills_the_old_one(client):
    login(client, make_user())
    first = emailed_code()

    client.post(reverse("authentication:resend_login_code"))
    second = emailed_code()

    assert first != second
    assert submit(client, first).status_code == 200
    assert "_auth_user_id" not in client.session

    assert submit(client, second).status_code == 302
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_resend_requires_post(client):
    """As a GET this gets fired by link prefetchers and email scanners, quietly
    rotating the code out from under someone mid-type."""
    login(client, make_user())

    response = client.get(reverse("authentication:resend_login_code"))

    assert response.status_code == 405


# --------------------------------------------------------------------------
# The email
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_the_email_carries_the_code_and_says_what_to_do_if_it_wasnt_you(client):
    user = make_user()
    login(client, user)

    sent = mail.outbox[0]

    assert sent.to == [user.email]
    assert emailed_code() in sent.subject, "the code belongs in the subject line"
    assert "didn't just try to log in" in sent.body
