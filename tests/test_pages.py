"""Project-level pages: the public landing page and the student dashboard.

These are placeholder shells — Sprint 2 and Sprint 4 wire them to real data.
The tests here cover the things that must hold regardless of what data arrives
later: the pages render, no template syntax leaks, and the dashboard is shut to
anonymous visitors.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

LEAKS = ["{#", "#}", "{%", "%}", "{{", "}}"]


def assert_renders_clean(html, screen):
    for token in LEAKS:
        assert token not in html, (
            f"{screen}: raw template syntax {token!r} leaked into the page. "
            f"If it's a multi-line {{# #}} comment, use {{% comment %}} instead."
        )


# --------------------------------------------------------------------------
# Landing page
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_landing_page_is_public(client):
    response = client.get(reverse("landing"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_landing_page_renders_clean(client):
    assert_renders_clean(client.get(reverse("landing")).content.decode(), "landing")


@pytest.mark.django_db
def test_landing_page_leads_to_register(client):
    """The whole point of the page: one obvious way in."""
    html = client.get(reverse("landing")).content.decode()
    assert reverse("authentication:register") in html
    assert "Get started" in html


@pytest.mark.django_db
def test_landing_page_uses_site_name_not_a_hardcoded_brand(client, settings):
    settings.SITE_NAME = "Zzyzx Test Brand"
    html = client.get(reverse("landing")).content.decode()
    assert "Zzyzx Test Brand" in html
    assert "Cybaroo" not in html


@pytest.mark.django_db
def test_landing_page_makes_no_external_requests(client):
    """CSP is default-src 'self'. Anything off-host is blocked by the browser,
    so a CDN reference here would render as a silently broken page."""
    html = client.get(reverse("landing")).content.decode()
    for marker in ["http://", "https://"]:
        assert marker not in html, f"landing page references an external URL ({marker})"


# --------------------------------------------------------------------------
# Dashboard
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_rejects_anonymous_visitors(client):
    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert "/admin/login/" in response.url, (
        "LOGIN_URL is temporary — when task 1.3 lands the real login view, "
        "update settings.LOGIN_URL and this assertion together."
    )


@pytest.mark.django_db
def test_dashboard_renders_for_a_logged_in_user(client):
    user = User.objects.create_user(email="student@example.com", password="x" * 14)
    client.force_login(user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_renders_clean(client):
    user = User.objects.create_user(email="student@example.com", password="x" * 14)
    client.force_login(user)

    assert_renders_clean(client.get(reverse("dashboard")).content.decode(), "dashboard")


# --------------------------------------------------------------------------
# Styleguide
# --------------------------------------------------------------------------


def render_styleguide():
    """Render the styleguide template directly.

    It can't be fetched by URL in tests: the route is registered only when
    settings.DEBUG is true, and the test runner forces it false — so the
    styleguide 404s here by design. Rendering the template is what actually
    matters anyway; it shipped once with an invented `split` filter that raised
    on every render, and no test noticed because no test rendered it.
    """
    from django.template.loader import render_to_string
    from django.test import RequestFactory

    request = RequestFactory().get("/styleguide/")
    return render_to_string("styleguide.html", request=request)


@pytest.mark.django_db
def test_styleguide_template_renders():
    assert "Component library" in render_styleguide()


@pytest.mark.django_db
def test_styleguide_renders_clean():
    assert_renders_clean(render_styleguide(), "styleguide")


# --------------------------------------------------------------------------
# No emoji anywhere
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_no_emoji_in_any_rendered_screen(client):
    """Icons are one SVG family; emoji render differently on every platform and
    would break the visual system the moment a user opened it on Windows."""
    import re

    user = User.objects.create_user(email="student@example.com", password="x" * 14)

    pages = {
        "landing": client.get(reverse("landing")).content.decode(),
        "register": client.get(reverse("authentication:register")).content.decode(),
        "styleguide": render_styleguide(),
    }
    client.force_login(user)
    pages["dashboard"] = client.get(reverse("dashboard")).content.decode()

    # Pictographs, emoticons, transport/map, dingbats, misc symbols.
    emoji = re.compile(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿️]"
    )
    for name, html in pages.items():
        found = emoji.findall(html)
        assert not found, f"{name}: emoji found {set(found)} — use an icon from _icons.html"


@pytest.mark.django_db
def test_dashboard_offers_exactly_one_primary_action(client):
    """One obvious action per screen is the rule the whole design rests on.
    If a second primary button appears, that rule has been broken."""
    user = User.objects.create_user(email="student@example.com", password="x" * 14)
    client.force_login(user)

    html = client.get(reverse("dashboard")).content.decode()

    assert html.count("cy-btn--primary") == 1
