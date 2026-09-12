"""The shared app shell (app_base.html) keys its logo + nav off the SECTION you
are in, not your role.

Regression guard for the bug where an administrator on the student dashboard got
a logo pointing at /manage/ and the admin console nav bleeding onto student
pages. The signal is `console` (set only by the staff console's _render), never
the user's role.
"""

import re

import pytest
from django.urls import reverse

from authentication.models import User, UserProfile


@pytest.fixture
def admin(db):
    user = User.objects.create_user(
        email="boss@example.com", password="x" * 14,
        first_name="Ada", role=User.Role.ADMINISTRATOR, is_verified=True,
    )
    user.is_staff = True
    user.save(update_fields=["is_staff"])
    UserProfile.objects.create(user=user)
    return user


def _brand_href(body):
    """The sidebar logo/wordmark link target."""
    m = re.search(r'class="cy-side__brand"\s+href="([^"]+)"', body)
    assert m, "sidebar brand link not found"
    return m.group(1)


# --- Administrator on the STUDENT side -------------------------------------

@pytest.mark.django_db
def test_admin_on_dashboard_logo_links_to_student_home(client, admin, modules):
    client.force_login(admin)
    body = client.get(reverse("dashboard")).content.decode()
    # The logo stays on the student side, not /manage/.
    assert _brand_href(body) == reverse("dashboard")
    assert reverse("staff:overview") not in body.split('class="cy-side__brand"')[1].split("</a>")[0]


@pytest.mark.django_db
def test_admin_on_dashboard_sees_student_nav_not_admin_nav(client, admin, modules):
    client.force_login(admin)
    body = client.get(reverse("dashboard")).content.decode()
    # Student nav is present...
    assert reverse("learn:browser") in body
    assert reverse("learn:progress") in body
    assert reverse("learn:badges") in body
    # ...and the admin console menu is NOT bleeding onto the student page.
    for name in ("staff:learners", "staff:organisations", "staff:content",
                 "staff:reports", "staff:activity"):
        assert reverse(name) not in body, name


@pytest.mark.django_db
def test_admin_on_dashboard_gets_one_discreet_console_link(client, admin, modules):
    client.force_login(admin)
    body = client.get(reverse("dashboard")).content.decode()
    # Exactly one discreet way back to the console, clearly labelled, in the foot.
    assert "Admin console" in body
    assert body.count(reverse("staff:overview")) == 1


# --- Administrator on the CONSOLE side (regression: unchanged) --------------

@pytest.mark.django_db
def test_admin_on_console_logo_links_to_overview(client, admin):
    client.force_login(admin)
    body = client.get(reverse("staff:overview")).content.decode()
    assert _brand_href(body) == reverse("staff:overview")
    # The console nav is present here (this is the admin section).
    assert reverse("staff:learners") in body
