"""Sprint 1.3 — sign-in.

The theme running through these: a password alone is not a session. Most of
what can go wrong here is something being let through one step early.
"""

import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

User = get_user_model()

PASSWORD = "correct-horse-battery"


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


@pytest.fixture
def instructor(db):
    return User.objects.create_user(
        email="instructor@example.com",
        password=PASSWORD,
        role=User.Role.INSTRUCTOR,
        is_verified=True,
    )


def login(client, email="meredith@example.com", password=PASSWORD, **extra):
    return client.post(
        reverse("authentication:login"),
        {"username": email, "password": password, **extra},
    )


# --------------------------------------------------------------------------
# The page
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_login_page_renders(client):
    assert client.get(reverse("authentication:login")).status_code == 200


@pytest.mark.django_db
def test_login_url_setting_points_at_our_login_view(client):
    """The /admin/login/ stopgap is gone. A student bounced off a protected
    page must land on our page, not Django's admin."""
    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("authentication:login"))
    assert "/admin/" not in response.url


# --------------------------------------------------------------------------
# Password
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_correct_password_sends_a_code_rather_than_logging_you_in(client, student):
    """The password is step one of two now, for every account. See
    test_two_factor.py for the code itself."""
    response = login(client)

    assert response.status_code == 302
    assert response.url == reverse("authentication:login_code")
    assert len(mail.outbox) == 1
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_wrong_password_is_rejected(client, student):
    response = login(client, password="not-the-password")

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_wrong_password_sends_no_email(client, student):
    """Otherwise the login form is a free way to post mail to any address that
    has an account here — a spam cannon with our name on the From line."""
    login(client, password="not-the-password")

    assert mail.outbox == []


@pytest.mark.django_db
def test_login_is_case_insensitive_on_email(client, student):
    """Registration lower-cases addresses and ModelBackend matches exactly, so
    without normalising here a phone's autocapitalise would lock someone out of
    their own account with 'no such user'."""
    response = login(client, email="Meredith@Example.COM")

    assert response.status_code == 302
    assert response.url == reverse("authentication:login_code")
    assert mail.outbox[0].to == ["meredith@example.com"]


@pytest.mark.django_db
def test_unverified_user_is_told_to_check_their_email(client):
    """ModelBackend rejects inactive users itself, so without special handling
    this reads as 'wrong password' and the user retries forever."""
    User.objects.create_user(
        email="unverified@example.com", password=PASSWORD, is_active=False
    )

    response = login(client, email="unverified@example.com")

    assert response.status_code == 200
    assert b"confirmed your email" in response.content
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_login_does_not_leak_the_password_back_into_the_page(client, student):
    response = login(client, password="wrong-but-memorable")

    assert b"wrong-but-memorable" not in response.content


# --------------------------------------------------------------------------
# Where people land
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_administrator_lands_on_the_in_platform_dashboard(client):
    """Administrators go to the Cybaroo Administrator dashboard, not Django's
    raw /admin/ (which stays reachable directly for data management)."""
    admin = User.objects.create_superuser(email="admin@example.com", password=PASSWORD)

    from authentication.utils import role_home_url

    assert role_home_url(admin) == reverse("staff:overview")


@pytest.mark.django_db
def test_administrator_without_staff_also_lands_on_the_dashboard(db):
    """The in-platform dashboard is role-gated, not is_staff-gated, so an
    ADMINISTRATOR without is_staff reaches it just the same (no dead end)."""
    from authentication.utils import role_home_url

    user = User.objects.create_user(
        email="roleonly@example.com",
        password=PASSWORD,
        role=User.Role.ADMINISTRATOR,
        is_staff=False,
    )

    assert role_home_url(user) == reverse("staff:overview")


def finish_with_code(client):
    """Type in whatever code was just emailed."""
    code = re.search(r"^\s{4}(\d{6})\s*$", mail.outbox[-1].body, re.M).group(1)
    return client.post(reverse("authentication:login_code"), {"code": code})


@pytest.mark.django_db
def test_next_survives_the_code_step(client, student):
    """?next= is captured at the password step and used two requests later, so
    it has to ride through the pending session. Easy thing to drop."""
    login(client, next="/dashboard/")

    response = finish_with_code(client)

    assert response.url == "/dashboard/"


@pytest.mark.django_db
def test_next_cannot_be_used_as_an_open_redirect(client, student):
    """Unvalidated ?next= turns our login page into a phishing kit hosted on
    our own domain — on a cyber-security training platform, no less.

    Validated at capture time, so the poisoned value never reaches the session
    and can't be honoured after the code check either.
    """
    login(client, next="https://evil.example/harvest")

    response = finish_with_code(client)

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert "evil.example" not in response.url


# --------------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_logout_requires_post(client, student):
    client.force_login(student)

    response = client.get(reverse("authentication:logout"))

    assert response.status_code == 405, "a GET logout can be fired by any <img> tag"
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_logout_via_post_ends_the_session(client, student):
    client.force_login(student)

    response = client.post(reverse("authentication:logout"))

    assert response.status_code == 302
    assert "_auth_user_id" not in client.session


# --------------------------------------------------------------------------
# Rate limiting (task 1.5, folded in — a bare login form is a brute-force target)
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_repeated_failures_are_rate_limited(client, student, rate_limiting):
    for _ in range(10):
        login(client, password="wrong")

    response = login(client, password="wrong")

    assert response.status_code == 429
    assert b"slow down" in response.content.lower()


@pytest.mark.django_db
def test_rate_limit_page_is_plain_language_not_a_stack_trace(
    client, student, rate_limiting
):
    for _ in range(11):
        login(client, password="wrong")

    response = login(client, password="wrong")

    assert response.status_code == 429
    assert b"Forbidden" not in response.content
    assert b"Traceback" not in response.content


@pytest.mark.django_db
def test_rate_limit_still_blocks_a_correct_password(client, student, rate_limiting):
    """Otherwise an attacker who finds the password on attempt 11 walks in —
    the limit would be protecting the guesses, not the account."""
    for _ in range(11):
        login(client, password="wrong")

    response = login(client)

    assert response.status_code == 429
    assert "_auth_user_id" not in client.session
