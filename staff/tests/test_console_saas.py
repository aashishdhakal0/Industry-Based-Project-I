"""The SaaS console layer: light/dark theming with a persisted toggle, the top
bar, KPI percent-change, the chart metric-toggle, and the goals widget.

Theme persistence is a real per-user preference (admin-only, POST+CSRF); the
server renders it on load. Chart deltas/goals are computed server-side from real
data, so they're unit-tested directly.
"""

import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import Organisation, User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult

PASSWORD = "correct-horse-battery"


def make_user(email, first, role=User.Role.STUDENT, **profile_kw):
    user = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Test",
        role=role, is_verified=True,
    )
    UserProfile.objects.create(user=user, **profile_kw)
    return user


@pytest.fixture
def world(db):
    admin = make_user("admin@example.com", "Ada", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])
    module = Module.objects.create(
        title="Network Security", order_index=1, is_published=True, created_by=admin
    )
    for n in (1, 2):
        Lesson.objects.create(module=module, lesson_number=n, title=f"L{n}")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)
    org = Organisation.objects.create(name="Riverside Council")
    finn = make_user("finn@example.com", "Finn", org=org, organisation="Riverside Council",
                     points=110, last_active=timezone.now())
    for lesson in module.lessons.all():
        ProgressRecord.objects.create(user=finn, lesson=lesson)
    QuizResult.objects.create(user=finn, quiz=quiz, score=95, passed=True, attempt_number=1)
    return {"admin": admin, "module": module, "org": org, "finn": finn}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Theme persistence (per user, admin-only) ------------------------------

def test_theme_defaults_to_dark(world):
    assert world["admin"].profile.console_theme == "dark"


def test_set_theme_persists_and_renders_on_load(client, world):
    as_admin(client, world)
    # Fetch-style POST persists and returns 204 (no reload).
    resp = client.post(reverse("staff:set_theme"), {"theme": "light"},
                       HTTP_X_REQUESTED_WITH="fetch")
    assert resp.status_code == 204
    world["admin"].profile.refresh_from_db()
    assert world["admin"].profile.console_theme == "light"
    # The server renders the remembered theme on the console root.
    body = client.get(reverse("staff:overview")).content.decode()
    assert 'data-theme="light"' in body


def test_set_theme_no_js_redirects_back(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:set_theme"),
                       {"theme": "light", "next": reverse("staff:overview")})
    assert resp.status_code == 302 and resp.url == reverse("staff:overview")


def test_set_theme_flips_when_no_value_given(client, world):
    as_admin(client, world)
    client.post(reverse("staff:set_theme"), {})   # no theme → flip from dark
    world["admin"].profile.refresh_from_db()
    assert world["admin"].profile.console_theme == "light"


def test_set_theme_is_admin_only(client, world):
    client.force_login(world["finn"])
    assert client.post(reverse("staff:set_theme"), {"theme": "light"}).status_code == 403
    world["finn"].profile.refresh_from_db()
    assert world["finn"].profile.console_theme == "dark"    # unchanged


def test_set_theme_rejects_get(client, world):
    as_admin(client, world)
    assert client.get(reverse("staff:set_theme")).status_code == 405


# --- Top bar + widgets on the page -----------------------------------------

def test_overview_has_the_topbar_and_theme_toggle(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:overview")).content.decode()
    assert "cy-topbar" in body
    assert 'name="q"' in body and "Search learners" in body   # search field
    assert "cy-themetoggle" in body                            # toggle form


def test_overview_leads_with_completion_and_charts(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:overview")).content.decode()
    # Completion-led hero + the two data visualisations.
    assert "Training completion" in body
    assert "cy-c-ring" in body                 # the completion ring
    assert "Activity over time" in body
    assert "Grade distribution" in body
    assert "Needs attention" in body           # consolidated attention section
    # The enriched hero: the cohort-engagement split bar (finn is a learner).
    assert "cy-c-ebar" in body
    assert "Where the cohort stands" in body
    # The old calendar and equal-weight KPI cards are gone.
    assert "cy-cal2__grid" not in body
    assert "cy-c-kpis" not in body


# --- Preserved functionality (no regression) -------------------------------

def test_existing_pages_still_work(client, world):
    as_admin(client, world)
    assert client.get(reverse("staff:overview")).status_code == 200
    assert client.get(reverse("staff:learners")).status_code == 200
    assert client.get(reverse("staff:organisations")).status_code == 200
    assert client.get(reverse("staff:learner_detail", args=[world["finn"].pk])).status_code == 200
    # A mutation still guards + works.
    resp = client.post(reverse("staff:nudge", args=[world["finn"].pk]))
    assert resp.status_code == 302
