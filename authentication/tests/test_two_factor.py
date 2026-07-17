"""Sprint 1.3 — two-factor authentication.

Role-based, deviating from the spec deliberately: mandatory for Instructors and
Administrators, optional for Students. See User.requires_2fa and the deviations
table in CLAUDE.md.

The tests that matter most are the ones asserting what is NOT possible: a
password-only session reaching a page, an unconfirmed device counting as a
factor, a pending login surviving indefinitely.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice

User = get_user_model()

PASSWORD = "correct-horse-battery"


def make_user(role, email=None, **extra):
    return User.objects.create_user(
        email=email or f"{role.lower()}@example.com",
        password=PASSWORD,
        role=role,
        is_verified=True,
        **extra,
    )


def confirmed_device(user):
    return TOTPDevice.objects.create(user=user, name="default", confirmed=True)


def current_token(device):
    """The code the user's app would be showing right now."""
    totp = TOTP(device.bin_key, device.step, device.t0, device.digits, device.drift)
    totp.time = __import__("time").time()
    return str(totp.token()).zfill(device.digits)


def login(client, user):
    return client.post(
        reverse("authentication:login"),
        {"username": user.email, "password": PASSWORD},
    )


# --------------------------------------------------------------------------
# The role rule — the deviation, pinned down
# --------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role,expected",
    [
        (User.Role.STUDENT, False),
        (User.Role.INSTRUCTOR, True),
        (User.Role.ADMINISTRATOR, True),
    ],
)
def test_which_roles_must_have_2fa(db, role, expected):
    assert make_user(role).requires_2fa is expected


@pytest.mark.django_db
def test_student_without_a_device_is_not_forced_into_setup(client):
    """The whole point of the deviation: an authenticator app is not the price
    of learning what a phishing email looks like."""
    student = make_user(User.Role.STUDENT)

    response = login(client, student)

    assert response.url == reverse("dashboard")
    assert client.session.get("_auth_user_id") == str(student.pk)


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.INSTRUCTOR, User.Role.ADMINISTRATOR])
def test_privileged_user_without_a_device_is_forced_into_setup(client, role):
    user = make_user(role)

    response = login(client, user)

    assert response.url == reverse("authentication:two_factor_setup")
    # And critically: they are NOT logged in yet.
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_privileged_user_mid_setup_cannot_reach_the_dashboard(client):
    """The half-authenticated window. If a pending login could reach a page,
    the mandatory part of mandatory 2FA would be decorative."""
    login(client, make_user(User.Role.INSTRUCTOR))

    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("authentication:login"))


# --------------------------------------------------------------------------
# Verifying
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_user_with_a_device_is_asked_for_a_code(client):
    student = make_user(User.Role.STUDENT)
    confirmed_device(student)

    response = login(client, student)

    assert response.url == reverse("authentication:two_factor_verify")
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_correct_code_completes_the_login(client):
    student = make_user(User.Role.STUDENT)
    device = confirmed_device(student)
    login(client, student)

    response = client.post(
        reverse("authentication:two_factor_verify"), {"token": current_token(device)}
    )

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert client.session.get("_auth_user_id") == str(student.pk)


@pytest.mark.django_db
def test_wrong_code_does_not_log_anyone_in(client):
    student = make_user(User.Role.STUDENT)
    confirmed_device(student)
    login(client, student)

    response = client.post(
        reverse("authentication:two_factor_verify"), {"token": "000000"}
    )

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_a_code_cannot_be_replayed(client):
    """TOTP codes are single-use within their window; django-otp tracks the
    last used counter. Replay would make a shoulder-surfed code reusable."""
    student = make_user(User.Role.STUDENT)
    device = confirmed_device(student)
    token = current_token(device)

    login(client, student)
    client.post(reverse("authentication:two_factor_verify"), {"token": token})
    client.post(reverse("authentication:logout"))

    login(client, student)
    response = client.post(
        reverse("authentication:two_factor_verify"), {"token": token}
    )

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_verify_without_a_pending_login_goes_back_to_login(client):
    response = client.get(reverse("authentication:two_factor_verify"))

    assert response.status_code == 302
    assert response.url == reverse("authentication:login")


@pytest.mark.django_db
def test_pending_login_expires(client, settings):
    """A password typed and then abandoned shouldn't stay usable all day on a
    shared machine."""
    from datetime import timedelta

    from django.utils import timezone

    student = make_user(User.Role.STUDENT)
    confirmed_device(student)
    login(client, student)

    session = client.session
    session["pending_2fa_started_at"] = (
        timezone.now() - timedelta(minutes=11)
    ).isoformat()
    session.save()

    response = client.get(reverse("authentication:two_factor_verify"))

    assert response.url == reverse("authentication:login")


# --------------------------------------------------------------------------
# Setting up
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_setup_page_offers_a_qr_and_a_typeable_key(client):
    """The manual key is not a nicety: a screen-reader user cannot scan a QR,
    so without it 2FA is simply shut to them."""
    login(client, make_user(User.Role.INSTRUCTOR))

    response = client.get(reverse("authentication:two_factor_setup"))

    assert response.status_code == 200
    assert b"data:image/png;base64," in response.content
    assert response.context["manual_key"]


@pytest.mark.django_db
def test_device_stays_unconfirmed_until_a_code_proves_it(client):
    """An unconfirmed device is a secret we generated that nobody scanned.
    Counting it as a second factor would mean reaching the setup page IS the
    second factor."""
    instructor = make_user(User.Role.INSTRUCTOR)
    login(client, instructor)
    client.get(reverse("authentication:two_factor_setup"))

    device = TOTPDevice.objects.get(user=instructor)
    assert device.confirmed is False

    from authentication.utils import confirmed_totp_device

    assert confirmed_totp_device(instructor) is None


@pytest.mark.django_db
def test_correct_code_confirms_the_device_and_finishes_the_login(client):
    instructor = make_user(User.Role.INSTRUCTOR)
    login(client, instructor)
    client.get(reverse("authentication:two_factor_setup"))
    device = TOTPDevice.objects.get(user=instructor)

    response = client.post(
        reverse("authentication:two_factor_setup"), {"token": current_token(device)}
    )

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    device.refresh_from_db()
    assert device.confirmed is True
    assert client.session.get("_auth_user_id") == str(instructor.pk)


@pytest.mark.django_db
def test_wrong_code_does_not_confirm_the_device(client):
    instructor = make_user(User.Role.INSTRUCTOR)
    login(client, instructor)
    client.get(reverse("authentication:two_factor_setup"))

    response = client.post(
        reverse("authentication:two_factor_setup"), {"token": "000000"}
    )

    assert response.status_code == 200
    assert TOTPDevice.objects.get(user=instructor).confirmed is False
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_a_signed_in_student_can_opt_in(client):
    """'Optional but encouraged' has to be a real door, not a line in a
    report."""
    student = make_user(User.Role.STUDENT)
    client.force_login(student)

    response = client.get(reverse("authentication:two_factor_setup"))
    assert response.status_code == 200

    device = TOTPDevice.objects.get(user=student)
    response = client.post(
        reverse("authentication:two_factor_setup"), {"token": current_token(device)}
    )

    assert response.status_code == 302
    device.refresh_from_db()
    assert device.confirmed is True


@pytest.mark.django_db
def test_setup_without_a_login_or_pending_session_is_refused(client):
    """Otherwise anyone could mint a device for... whom, exactly?"""
    response = client.get(reverse("authentication:two_factor_setup"))

    assert response.status_code == 302
    assert response.url == reverse("authentication:login")


@pytest.mark.django_db
def test_setup_does_not_mint_a_second_device_on_reload(client):
    instructor = make_user(User.Role.INSTRUCTOR)
    login(client, instructor)

    client.get(reverse("authentication:two_factor_setup"))
    client.get(reverse("authentication:two_factor_setup"))

    assert TOTPDevice.objects.filter(user=instructor).count() == 1
