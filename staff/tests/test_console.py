"""The upgraded console: search, quick-filters, pagination, organisations,
activity log, drill-down back-link, and inline-confirm markup.

Security is re-asserted for the new pages (real 403 for non-admins), and the
search/filter/paginate path stays on the single bounded aggregation.
"""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult

PASSWORD = "correct-horse-battery"


def student(email, first, org="", points=0, days=None):
    from authentication.models import Organisation

    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Doe",
        role=User.Role.STUDENT, is_verified=True,
    )
    last = timezone.now() - timedelta(days=days) if days is not None else None
    org_obj = Organisation.objects.get_or_create(name=org)[0] if org else None
    UserProfile.objects.create(
        user=u, organisation=org, org=org_obj, points=points, last_active=last
    )
    return u


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)

    module = Module.objects.create(title="M1", order_index=1, is_published=True, created_by=admin)
    for n in (1, 2):
        Lesson.objects.create(module=module, lesson_number=n, title=f"L{n}")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)

    # Ada Council: one finisher (distinction), one dormant.
    fin = student("finn@council.gov.au", "Finn", org="Riverside Council", points=110, days=1)
    for lesson in module.lessons.all():
        ProgressRecord.objects.create(user=fin, lesson=lesson)
    QuizResult.objects.create(user=fin, quiz=quiz, score=95, passed=True, attempt_number=1)

    dorm = student("dana@council.gov.au", "Dana", org="Riverside Council", days=30)  # dormant
    # Milkwood Cafe: one who never started.
    student("mo@milkwood.com.au", "Mo", org="Milkwood Cafe")

    return {"admin": admin, "module": module, "finn": fin, "dana": dorm}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Access control on the new pages ---------------------------------------

@pytest.mark.parametrize("name", ["staff:organisations", "staff:activity"])
def test_new_pages_are_admin_only(client, world, name):
    # Student → 403
    client.force_login(world["finn"])
    assert client.get(reverse(name)).status_code == 403
    # Anonymous → login redirect
    client.logout()
    resp = client.get(reverse(name))
    assert resp.status_code == 302 and reverse("authentication:login") in resp.url
    # Admin → 200
    as_admin(client, world)
    assert client.get(reverse(name)).status_code == 200


# --- Search ----------------------------------------------------------------

def test_search_matches_name_email_and_org(world):
    from staff import services

    rows = services.collect_learners()
    assert {r.user.email for r in services.search_learners(rows, "finn")} == {"finn@council.gov.au"}
    assert {r.user.email for r in services.search_learners(rows, "milkwood")} == {"mo@milkwood.com.au"}
    # Organisation search returns everyone in it.
    assert len(services.search_learners(rows, "riverside")) == 2


def test_search_on_the_page_narrows_rows(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?q=milkwood").content.decode()
    assert "mo@milkwood.com.au" in body
    assert "finn@council.gov.au" not in body


# --- Quick filters ---------------------------------------------------------

@pytest.mark.parametrize(
    "key,expected",
    [
        ("completed", {"finn@council.gov.au"}),
        ("not_started", {"mo@milkwood.com.au"}),
        ("dormant", {"dana@council.gov.au"}),
        ("distinction", {"finn@council.gov.au"}),
    ],
)
def test_quick_filters_narrow_correctly(world, key, expected):
    from staff import services

    rows = services.collect_learners()
    got = {r.user.email for r in services.filter_learners(rows, key)}
    assert got == expected


def test_needs_attention_filter_page(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?filter=attention").content.decode()
    assert "dana@council.gov.au" in body      # dormant → needs attention
    assert "finn@council.gov.au" not in body


# --- Pagination ------------------------------------------------------------

def test_pagination_splits_and_preserves_params(client, db):
    admin = User.objects.create_user(
        email="a@example.com", password=PASSWORD, role=User.Role.ADMINISTRATOR,
        is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)
    for i in range(30):
        student(f"s{i:02d}@example.com", f"S{i:02d}")
    client.force_login(admin)

    p1 = client.get(reverse("staff:learners") + "?sort=name")
    assert p1.context["page_obj"].paginator.num_pages == 2
    assert len(p1.context["page_obj"].object_list) == 25

    p2 = client.get(reverse("staff:learners") + "?sort=name&page=2")
    assert len(p2.context["page_obj"].object_list) == 5
    # Sort param carried into the page-2 links.
    assert "sort=name" in p2.content.decode()


# --- Organisation rollup ---------------------------------------------------

def test_organisation_rollup_math(world):
    from staff import services

    orgs = {o["name"]: o for o in services.organisation_rollup(services.collect_learners())}
    council = orgs["Riverside Council"]
    assert council["learners"] == 2
    assert council["completed"] == 1          # Finn
    assert council["completion"] == 50        # 1 of 2
    assert council["avg_score"] == 95         # only Finn has a grade
    assert council["attention"] == 1          # Dana dormant

    cafe = orgs["Milkwood Cafe"]
    assert cafe["learners"] == 1
    assert cafe["avg_score"] is None          # never attempted


def test_organisations_page_lists_orgs(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:organisations")).content.decode()
    assert "Riverside Council" in body
    assert "Milkwood Cafe" in body


# --- Activity log ----------------------------------------------------------

def test_activity_log_shows_actions(client, world):
    from staff import services
    from staff.models import AdminAction

    services.log_action(world["admin"], AdminAction.Kind.NUDGE, "Sent a nudge to finn@council.gov.au",
                        target_user=world["finn"])
    as_admin(client, world)
    body = client.get(reverse("staff:activity")).content.decode()
    assert "Sent a nudge to finn@council.gov.au" in body


# --- Drill-down + confirmation markup --------------------------------------

def test_learner_link_carries_back_and_detail_uses_it(client, world):
    as_admin(client, world)
    # The list links carry the current query as ?back=...
    listing = client.get(reverse("staff:learners") + "?filter=attention&sort=grade").content.decode()
    assert "back=" in listing
    # The detail page's back link returns to the list with that query.
    detail = client.get(
        reverse("staff:learner_detail", args=[world["finn"].pk]) + "?back=filter%3Dattention%26sort%3Dgrade"
    ).content.decode()
    assert "Back to learners" in detail
    assert "filter=attention" in detail


def test_important_actions_have_confirm_markup(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learner_detail", args=[world["finn"].pk])).content.decode()
    # Deactivate and change-role forms carry a data-confirm for the JS confirm step.
    assert 'data-confirm="Deactivate this account' in body
    assert 'data-confirm="Change this learner' in body
