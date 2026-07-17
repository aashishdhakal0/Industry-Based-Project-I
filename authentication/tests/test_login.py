"""Sprint 1.3 — sign-in.

The theme running through these: a password alone is not a session. Most of
what can go wrong here is something being let through one step early.
"""

import pytest
from django.contrib.auth import get_user_model
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
def test_student_without_2fa_logs_straight_in(client, student):
    response = login(client)

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert client.session.get("_auth_user_id") == str(student.pk)


@pytest.mark.django_db
def test_wrong_password_is_rejected(client, student):
    response = login(client, password="not-the-password")

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_login_is_case_insensitive_on_email(client, student):
    """Registration lower-cases addresses and ModelBackend matches exactly, so
    without normalising here a phone's autocapitalise would lock someone out of
    their own account with 'no such user'."""
    response = login(client, email="Meredith@Example.COM")

    assert response.status_code == 302
    assert client.session.get("_auth_user_id") == str(student.pk)


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
def test_administrator_lands_in_the_admin(client):
    admin = User.objects.create_superuser(email="admin@example.com", password=PASSWORD)

    response = login(client, email="admin@example.com")

    # Superusers require 2FA, so they go via setup rather than straight in.
    assert response.url == reverse("authentication:two_factor_setup")

    # ...and role_home_url is what decides the eventual destination.
    from authentication.utils import role_home_url

    assert role_home_url(admin) == reverse("admin:index")


@pytest.mark.django_db
def test_administrator_without_staff_does_not_land_in_a_dead_end(db):
    """An ADMINISTRATOR without is_staff would be turned away by the admin's
    own login. Send them somewhere that works instead."""
    from authentication.utils import role_home_url

    user = User.objects.create_user(
        email="roleonly@example.com",
        password=PASSWORD,
        role=User.Role.ADMINISTRATOR,
        is_staff=False,
    )

    assert role_home_url(user) == reverse("dashboard")


@pytest.mark.django_db
def test_next_parameter_is_honoured(client, student):
    response = login(client, next="/dashboard/")

    assert response.url == "/dashboard/"


@pytest.mark.django_db
def test_next_cannot_be_used_as_an_open_redirect(client, student):
    """Unvalidated ?next= turns our login page into a phishing kit hosted on
    our own domain — on a cyber-security training platform, no less."""
    response = login(client, next="https://evil.example/harvest")

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
