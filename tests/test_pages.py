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
# The shared shell — nav
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_mobile_nav_toggle_is_wired_to_its_panel(client):
    """The hamburger toggles a panel by id. If the button's aria-controls and
    the panel's id drift apart, the menu silently stops working for assistive
    tech — and there's no visual sign on desktop, where the toggle is hidden."""
    html = client.get(reverse("landing")).content.decode()

    assert 'aria-controls="cy-nav-menu"' in html
    assert 'id="cy-nav-menu"' in html
    # Ships hidden so a no-JS visitor never meets a dead button (footer is their
    # fallback); cybaroo.js removes the attribute.
    assert 'class="cy-nav__toggle"' in html
    assert " hidden" in html


# --------------------------------------------------------------------------
# Landing page
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_module_tiles_link_to_login_for_now(client):
    """The cards are clickable; until modules exist they point at login. A test
    because 'they'll route to the real module later' is exactly the kind of
    placeholder that gets forgotten."""
    for name in ["landing", "modules"]:
        html = client.get(reverse(name)).content.decode()
        assert 'class="cy-module-link" href="/login/"' in html, name
        # The open tile shows an explicit call to action.
        assert "cy-module__cta" in html, name


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
    """The /admin/login/ stopgap is gone as of task 1.3 — anonymous visitors
    now land on our own login page, with ?next= back to where they were going."""
    response = client.get(reverse("dashboard"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("authentication:login"))
    assert "next=/dashboard/" in response.url


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
# Contrast — the two failures that were found by measuring, not looking
# --------------------------------------------------------------------------


def _contrast(fg, bg):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def lum(h):
        h = h.lstrip("#")
        r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def _token(name):
    """Read a custom property's value straight out of the stylesheet."""
    import pathlib
    import re

    css = pathlib.Path("static/css/cybaroo.css").read_text()
    match = re.search(rf"{re.escape(name)}:\s*([^;]+);", css)
    assert match, f"{name} is not defined in cybaroo.css"
    return match.group(1).strip()


def test_input_borders_meet_wcag_non_text_contrast():
    """WCAG 1.4.11: the boundary of a control you're meant to find and type in
    needs 3:1 against its surroundings.

    This shipped at 1.58:1 — which is why the fields read as "almost the same
    as the background". They were. The fix is a token, so the test guards the
    token rather than a screenshot.
    """
    line = _token("--cy-field-line")
    for surface in ("#191926", "#12121c", "#0b0b12"):
        ratio = _contrast(line, surface)
        assert ratio >= 3.0, (
            f"--cy-field-line ({line}) is {ratio:.2f}:1 against {surface} — "
            f"WCAG 1.4.11 requires 3:1 for input boundaries."
        )


def _gradient_stops(token_name):
    import re

    stops = re.findall(r"#[0-9a-fA-F]{6}", _token(token_name))
    assert len(stops) == 2, f"expected two stops in {token_name}, got {stops}"
    return stops


def test_cta_gradient_carries_white_text_legibly():
    """The primary button is WHITE on the deep gradient (--cy-grad-cta).

    This took three attempts, and the test exists so the next person doesn't
    repeat them:
      bright fill + white ink -> 1.81:1. Cyan is far too luminous.
      bright fill + dark ink  -> 7.21:1 on paper, still read as muddy.
      deep fill + white ink   -> 7.10:1, and reads sharp. This is what ships.
    """
    for stop in _gradient_stops("--cy-grad-cta"):
        ratio = _contrast("#ffffff", stop)
        assert ratio >= 4.5, (
            f"white on {stop} is {ratio:.2f}:1 — the CTA label fails AA. "
            f"Deepen the gradient rather than switching the label to dark ink; "
            f"dark-on-bright has been tried twice and reads muddy."
        )


def test_display_gradient_stays_legible_as_text_on_the_dark_page():
    """--cy-grad is the opposite job: bright, because it's text ON the near-
    black page (the hero word, the big stat numbers). If someone 'unifies' the
    two gradients, one of these two tests fails — which is the point."""
    bg = _token("--cy-bg")
    for stop in _gradient_stops("--cy-grad"):
        ratio = _contrast(stop, bg)
        assert ratio >= 4.5, (
            f"{stop} as text on {bg} is {ratio:.2f}:1. --cy-grad must stay "
            f"bright; it is not the button fill."
        )


def test_the_two_gradients_have_not_been_merged():
    """They look redundant and they are not. --cy-grad is light (text on dark),
    --cy-grad-cta is dark (fill under white text). Same hues, inverted."""
    assert _token("--cy-grad") != _token("--cy-grad-cta")


def test_every_animation_references_keyframes_that_exist():
    """An `animation: foo` naming keyframes that don't exist is a silent no-op.

    This bit us for real. `cy-spin` was defined alongside the original hero orb;
    when that scene was deleted the keyframes went with it, and the level
    badge's orbit track quietly stopped rotating. Its counter-rotation survived,
    so the badge span on the spot instead of orbiting — exactly the symptom
    reported, with no error anywhere and nothing in the test suite to catch it.

    Every animation name in the stylesheet must resolve.
    """
    import pathlib
    import re

    css = pathlib.Path("static/css/cybaroo.css").read_text()
    code = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    defined = set(re.findall(r"@keyframes\s+([\w-]+)", code))
    used = set()
    for value in re.findall(r"animation:\s*([^;]+);", code):
        # Drop var(--cy-ease) and friends first: those are timing functions and
        # delays sitting in the same shorthand, not keyframes names. Without
        # this the check reports --cy-ease as a missing animation, which sends
        # the next person hunting for a bug that isn't there.
        value = re.sub(r"var\([^)]*\)", "", value)
        for word in re.findall(r"\bcy-[\w-]+", value):
            used.add(word)

    missing = used - defined
    assert not missing, (
        f"animations reference keyframes that do not exist: {sorted(missing)}. "
        f"They fail silently — the element simply never animates."
    )


def test_every_vendored_font_referenced_in_css_exists_on_disk():
    """A missing @font-face src fails silently — the browser just falls back to
    Georgia and the identity quietly evaporates."""
    import pathlib
    import re

    css = pathlib.Path("static/css/cybaroo.css").read_text()
    for ref in re.findall(r'url\("\.\./fonts/([^"]+)"\)', css):
        assert (pathlib.Path("static/fonts") / ref).exists(), (
            f"cybaroo.css references fonts/{ref}, which is not vendored"
        )


@pytest.mark.parametrize("face,glob", [("Space Grotesk", "space-grotesk*"), ("Fraunces", "fraunces*")])
def test_no_retired_typeface_is_still_in_use(face, glob):
    """Retired faces must leave no live reference — their files are gone, so a
    survivor would silently fall back to Georgia and the identity evaporates.

    Checks usage, not mentions: the comments explaining why each face was
    dropped are the most useful sentences in that part of the file, and an
    assertion forbidding you to name what you replaced would delete your own
    reasoning.
    """
    import pathlib
    import re

    css = pathlib.Path("static/css/cybaroo.css").read_text()
    # Strip comments first — what's left is the code that actually runs.
    code = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    assert face not in code, f"{face} is still referenced in live CSS"
    assert not list(pathlib.Path("static/fonts").glob(glob))


# --------------------------------------------------------------------------
# Stats
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_stat_numbers_are_real_in_the_markup_not_filled_in_by_javascript(client):
    """The count-up animates from 0 up to the figure already in the HTML.

    If the markup shipped "0" and JavaScript filled it in, then every visitor
    without JS — and everyone with reduced motion — would read that Australia
    had zero cybercrime reports. These are real ASD figures on a public page
    for a real client; the truth goes in the HTML and the animation is the
    enhancement.
    """
    html = client.get(reverse("landing")).content.decode()

    assert ">84,700<" in html
    assert ">$56,600<" in html
    assert 'data-count-to="84700"' in html


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
    """One obvious action per screen is the rule the whole design rests on. On
    the dashboard that's the single Resume button — if a second primary appears,
    the rule has been broken."""
    from modules.models import Lesson, Module

    author = User.objects.create_user(email="a@example.com", password="x" * 14)
    module = Module.objects.create(
        title="M1", order_index=1, is_published=True, created_by=author
    )
    Lesson.objects.create(module=module, lesson_number=1, title="L1", body_text="<p>x</p>")

    user = User.objects.create_user(email="student@example.com", password="x" * 14)
    client.force_login(user)

    html = client.get(reverse("dashboard")).content.decode()

    assert html.count("cy-btn--primary") == 1
