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
def test_landing_page_loads_no_external_resources(client):
    """CSP is default-src 'self'. Anything the page *fetches* from another host
    is blocked by the browser, so a CDN reference would render as a silently
    broken page.

    This checks resource loads, not links. An <a href> to an external site is
    navigation — CSP has no opinion on it, and the ASD citation on this page is
    exactly that. An earlier version of this test banned every "https://" in
    the markup, which would have made citing a source impossible: the strictest
    assertion is not always the right one.
    """
    import re

    html = client.get(reverse("landing")).content.decode()

    offenders = []
    # src="..." on any element, href on <link> (stylesheets), and url() in CSS.
    offenders += re.findall(r'src="(https?://[^"]+)"', html)
    offenders += re.findall(r'<link[^>]+href="(https?://[^"]+)"', html)
    offenders += re.findall(r"url\((https?://[^)]+)\)", html)

    assert not offenders, (
        f"landing page loads external resources, which CSP will block: {offenders}"
    )


@pytest.mark.django_db
def test_landing_page_cites_its_source_for_every_statistic(client):
    """The stats are real ASD figures. A number on a marketing page without a
    source and a reporting period is a claim we can't back — and these get
        stale annually, so the period has to be visible, not implied."""
    html = client.get(reverse("landing")).content.decode()

    assert "84,700" in html
    assert "ASD Annual Cyber Threat Report" in html
    assert "2024–25" in html
    assert "cyber.gov.au" in html, "the figures must link to the source"


# --------------------------------------------------------------------------
# About and Modules
# --------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["about", "modules"])
def test_public_pages_render(client, name):
    assert client.get(reverse(name)).status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["about", "modules"])
def test_public_pages_render_clean(client, name):
    assert_renders_clean(client.get(reverse(name)).content.decode(), name)


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["landing", "about", "modules"])
def test_every_public_page_carries_the_site_nav(client, name):
    html = client.get(reverse(name)).content.decode()
    for target in ["landing", "about", "modules"]:
        assert reverse(target) in html, f"{name} is missing a nav link to {target}"


@pytest.mark.django_db
def test_module_names_come_from_one_source(client):
    """The six titles appear on the landing page, the modules page, the
    dashboard and the styleguide. They're defined once in
    nstp/placeholder_content.py precisely so four copies can't drift apart —
    this fails if someone hard-codes them back into a template."""
    from django.utils.html import escape

    from nstp.placeholder_content import MODULES

    landing = client.get(reverse("landing")).content.decode()
    modules = client.get(reverse("modules")).content.decode()

    # escape(), because two titles contain "&" and Django autoescapes it to
    # "&amp;" — which is the template engine protecting us, not a bug. Asserting
    # on the raw string would be asserting that autoescaping is off.
    for m in MODULES:
        title = escape(m["title"])
        assert title in landing, f"{m['title']} missing from the landing page"
        assert title in modules, f"{m['title']} missing from the modules page"
        assert escape(m["subtitle"]) in modules, f"{m['title']} has no subtitle"


@pytest.mark.django_db
def test_modules_page_shows_the_sequential_lock_honestly(client):
    """Only module one is open. Showing six unlocked tiles would misrepresent
    how the platform actually behaves."""
    html = client.get(reverse("modules")).content.decode()

    assert html.count("cy-module--locked") == 5
    assert html.count("cy-chip--locked") == 5


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
