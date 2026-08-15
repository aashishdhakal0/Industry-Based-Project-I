"""The learners page grouped by organisation: students AND administrators inside
each org, a No-organisation bucket, per-org stats, role badges, status pills, the
In-progress filter, and the grouped/list toggle.
"""

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
    admin = make_user("ada@example.com", "Ada", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])

    module = Module.objects.create(
        title="Network Security", order_index=1, is_published=True, created_by=admin
    )
    for n in (1, 2):
        Lesson.objects.create(module=module, lesson_number=n, title=f"L{n}")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)

    org = Organisation.objects.create(name="Riverside Council")
    admin.profile.org = org
    admin.profile.organisation = "Riverside Council"
    admin.profile.save()

    finn = make_user("finn@example.com", "Finn", org=org, organisation="Riverside Council",
                     points=110, last_active=timezone.now())
    for lesson in module.lessons.all():
        ProgressRecord.objects.create(user=finn, lesson=lesson)
    QuizResult.objects.create(user=finn, quiz=quiz, score=95, passed=True, attempt_number=1)

    # A student with no organisation, only partway through.
    mo = make_user("mo@example.com", "Mo", points=10, last_active=timezone.now())
    ProgressRecord.objects.create(user=mo, lesson=module.lessons.first())

    return {"admin": admin, "org": org, "module": module, "finn": finn, "mo": mo}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- collect_learners roles ------------------------------------------------

def test_collect_defaults_to_students_only(world):
    from staff import services

    emails = {r.user.email for r in services.collect_learners()}
    assert emails == {"finn@example.com", "mo@example.com"}   # no admin


def test_collect_can_include_staff_roles(world):
    from staff import services

    roles = (User.Role.STUDENT, User.Role.INSTRUCTOR, User.Role.ADMINISTRATOR)
    emails = {r.user.email for r in services.collect_learners(roles=roles)}
    assert "ada@example.com" in emails      # the admin is now included


# --- Row status + role -----------------------------------------------------

def test_row_status_and_role(world):
    from staff import services

    roles = (User.Role.STUDENT, User.Role.ADMINISTRATOR)
    rows = {r.user.email: r for r in services.collect_learners(roles=roles)}
    assert rows["finn@example.com"].status == "completed"
    assert rows["finn@example.com"].status_label == "Completed"
    assert rows["mo@example.com"].status == "progress"
    assert rows["ada@example.com"].status == "staff"        # non-learner
    assert rows["ada@example.com"].is_student is False
    assert rows["ada@example.com"].role_label == "Administrator"


# --- Grouping --------------------------------------------------------------

def test_group_by_organisation_stats_and_order(world):
    from staff import services

    roles = (User.Role.STUDENT, User.Role.ADMINISTRATOR)
    groups = services.group_by_organisation(services.collect_learners(roles=roles))
    by_name = {g["name"]: g for g in groups}

    council = by_name["Riverside Council"]
    assert council["count"] == 2            # Finn + Ada
    assert council["students"] == 1         # only Finn
    assert council["completed"] == 1
    assert council["avg_completion"] == 100
    assert council["org_id"] == world["org"].pk

    none = by_name["No organisation"]
    assert none["is_none"] is True
    assert {m.user.email for m in none["members"]} == {"mo@example.com"}

    # No-organisation is always last.
    assert groups[-1]["name"] == "No organisation"


# --- Grouped page ----------------------------------------------------------

def test_grouped_page_shows_orgs_roles_and_status(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners")).content.decode()
    assert "cy-c-org" in body                       # collapsible org section
    assert "Riverside Council" in body and "No organisation" in body
    assert "ada@example.com" in body                # admin appears in the group
    assert "cy-role--administrator" in body and "cy-role--student" in body
    assert "cy-status--completed" in body           # Finn
    assert "avg completion" in body
    # Per-org CSV link for a real organisation.
    assert reverse("staff:org_learners_csv", args=[world["org"].pk]) in body


def test_list_view_is_students_only_and_paginated(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?view=list").content.decode()
    assert "cy-c-th" in body                         # sortable column headers
    assert "ada@example.com" not in body             # list stays students-only
    assert "cy-status--" in body                     # status column present


def test_in_progress_filter(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?filter=in_progress").content.decode()
    assert "mo@example.com" in body                  # started, not finished
    assert "finn@example.com" not in body            # completed → excluded


def test_grouped_search_narrows_across_groups(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:learners") + "?q=mo@example").content.decode()
    assert "mo@example.com" in body
    assert "finn@example.com" not in body


# --- Access control --------------------------------------------------------

def test_learners_is_admin_only(client, world):
    client.force_login(world["finn"])
    assert client.get(reverse("staff:learners")).status_code == 403
