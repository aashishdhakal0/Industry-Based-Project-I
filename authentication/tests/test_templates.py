"""Every screen must render clean — no template syntax leaking to the user.

This exists because it happened: three `{# ... #}` comments wrapped onto a
second line and rendered as visible text next to the form labels, one of them
in base.html and so on every page in the platform.

Django only strips `{# #}` when it opens and closes on the *same line*. A
wrapped one is not a comment — it is literal text. Use `{% comment %}` for
anything multi-line.
"""

import pathlib
import re

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from authentication.tokens import make_verification_token

User = get_user_model()

# Anything that means "the template engine didn't finish its job".
LEAKS = ["{#", "#}", "{%", "%}", "{{", "}}"]

TEMPLATE_DIRS = ["templates", "authentication/templates"]


def assert_renders_clean(html, screen):
    for token in LEAKS:
        assert token not in html, (
            f"{screen}: raw template syntax {token!r} leaked into the page. "
            f"If it's a multi-line {{# #}} comment, use {{% comment %}} instead."
        )


@pytest.fixture
def unverified_user(db):
    return User.objects.create_user(
        email="screens@example.com", password="x" * 14, is_active=False
    )


@pytest.mark.django_db
def test_register_screen_renders_clean(client):
    assert_renders_clean(
        client.get(reverse("authentication:register")).content.decode(), "register"
    )


@pytest.mark.django_db
def test_register_screen_with_errors_renders_clean(client):
    """The error branch is a separate path through the template."""
    response = client.post(reverse("authentication:register"), {"email": "nope"})
    assert_renders_clean(response.content.decode(), "register (with errors)")


@pytest.mark.django_db
def test_check_inbox_screen_renders_clean(client):
    assert_renders_clean(
        client.get(reverse("authentication:check_inbox")).content.decode(),
        "check-inbox",
    )


@pytest.mark.django_db
def test_verified_screen_renders_clean(client, unverified_user):
    url = reverse("authentication:verify", args=[make_verification_token(unverified_user)])
    assert_renders_clean(client.get(url).content.decode(), "verified")


@pytest.mark.django_db
def test_link_invalid_screen_renders_clean(client):
    response = client.get(reverse("authentication:verify", args=["garbage-token"]))
    assert response.status_code == 400
    assert_renders_clean(response.content.decode(), "link-invalid")


@pytest.mark.django_db
def test_link_expired_screen_renders_clean(client, unverified_user):
    """Force expiry by asking the view to honour a zero-second window."""
    from authentication import views

    token = make_verification_token(unverified_user)
    original = views.read_verification_token
    try:
        views.read_verification_token = lambda t: original(t, max_age=-1)
        response = client.get(reverse("authentication:verify", args=[token]))
    finally:
        views.read_verification_token = original

    assert response.status_code == 410
    assert_renders_clean(response.content.decode(), "link-expired")


def test_no_template_has_a_multiline_hash_comment():
    """Catch the mistake at the source, not just where it happens to render.

    A `{# ... #}` that opens on one line and closes on another is not a comment
    to Django — it is text. This walks every template so a new one can't
    reintroduce the bug on a page no test happens to render.
    """
    offenders = []
    for directory in TEMPLATE_DIRS:
        for path in pathlib.Path(directory).glob("**/*.html"):
            for lineno, line in enumerate(path.read_text().splitlines(), 1):
                if "{#" in line and "#}" not in line.split("{#", 1)[1]:
                    offenders.append(f"{path}:{lineno}")

    assert not offenders, (
        "multi-line {# #} comments render as visible text — use {% comment %}:\n  "
        + "\n  ".join(offenders)
    )


def test_verification_email_body_renders_clean():
    """The email is a template too, and nobody looks at it in a browser."""
    from django.conf import settings
    from django.template.loader import render_to_string

    body = render_to_string(
        "authentication/email/verify_email.txt",
        {
            "first_name": "Meredith",
            "verify_url": "https://example.com/verify/token/",
            "site_name": settings.SITE_NAME,
        },
    )
    assert_renders_clean(body, "verification email")
    assert settings.SITE_NAME in body
