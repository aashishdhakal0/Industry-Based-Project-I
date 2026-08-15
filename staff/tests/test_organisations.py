"""Organisation management: create, edit, assign/reassign/remove, and the
managed rollup. Plus access control (real 403), audit logging, and the FK/text
mirror staying in step.
"""

import pytest
from django.core import mail
from django.urls import reverse

from authentication.models import Organisation, User, UserProfile
from staff.models import AdminAction

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
    council = Organisation.objects.create(name="Riverside Council", sector="Local council")
    sam = make_user("sam@example.com", "Sam", org=council, organisation="Riverside Council")
    dana = make_user("dana@example.com", "Dana")   # unassigned
    return {"admin": admin, "council": council, "sam": sam, "dana": dana}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Access control (real 403 / login redirect) ----------------------------

def test_org_pages_forbid_students(client, world):
    client.force_login(world["sam"])
    urls = [
        reverse("staff:organisations"),
        reverse("staff:org_new"),
        reverse("staff:org_detail", args=[world["council"].pk]),
    ]
    for url in urls:
        assert client.get(url).status_code == 403
    assert client.post(reverse("staff:assign_org", args=[world["sam"].pk])).status_code == 403


def test_org_pages_send_anonymous_to_login(client, world):
    resp = client.get(reverse("staff:organisations"))
    assert resp.status_code == 302 and reverse("authentication:login") in resp.url


# --- Create ----------------------------------------------------------------

def test_create_organisation(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:org_new"), {
        "name": "Milkwood Cafe", "sector": "Small business",
        "contact_email": "hi@milkwood.example", "notes": "Cohort of 4.",
    })
    assert resp.status_code == 302
    org = Organisation.objects.get(name="Milkwood Cafe")
    assert org.sector == "Small business"
    assert AdminAction.objects.filter(action=AdminAction.Kind.CREATE_ORG).exists()


def test_create_rejects_duplicate_name(client, world):
    as_admin(client, world)
    before = Organisation.objects.count()
    resp = client.post(reverse("staff:org_new"), {"name": "Riverside Council"})
    assert resp.status_code == 200               # re-rendered with the error
    assert Organisation.objects.count() == before
    assert b"already exists" in resp.content


# --- Edit details ----------------------------------------------------------

def test_edit_organisation_details(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:org_detail", args=[world["council"].pk]),
        {"name": "Riverside City Council", "sector": "Local government",
         "contact_email": "", "notes": ""},
    )
    assert resp.status_code == 302
    world["council"].refresh_from_db()
    assert world["council"].name == "Riverside City Council"
    assert world["council"].sector == "Local government"
    assert AdminAction.objects.filter(action=AdminAction.Kind.EDIT_ORG).exists()


# --- Assign / reassign / remove --------------------------------------------

def test_assign_learner_sets_fk_and_text_mirror(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:assign_org", args=[world["dana"].pk]),
        {"org": world["council"].pk},
    )
    assert resp.status_code == 302
    profile = world["dana"].profile
    profile.refresh_from_db()
    assert profile.org_id == world["council"].pk
    assert profile.organisation == "Riverside Council"      # mirror kept in step
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.ASSIGN_ORG, target_user=world["dana"]
    ).exists()


def test_reassign_learner_to_a_different_org(client, world):
    as_admin(client, world)
    cafe = Organisation.objects.create(name="Milkwood Cafe")
    client.post(reverse("staff:assign_org", args=[world["sam"].pk]), {"org": cafe.pk})
    profile = world["sam"].profile
    profile.refresh_from_db()
    assert profile.org_id == cafe.pk
    assert profile.organisation == "Milkwood Cafe"


def test_remove_learner_from_org_clears_both(client, world):
    as_admin(client, world)
    resp = client.post(
        reverse("staff:assign_org", args=[world["sam"].pk]),
        {"org": "", "from_org": world["council"].pk},
    )
    # Removing from the org page returns to that org page.
    assert resp.status_code == 302
    assert reverse("staff:org_detail", args=[world["council"].pk]) in resp.url
    profile = world["sam"].profile
    profile.refresh_from_db()
    assert profile.org is None
    assert profile.organisation == ""


# --- The managed rollup + members ------------------------------------------

def test_managed_rollup_includes_empty_orgs_and_counts(world):
    from staff import services

    Organisation.objects.create(name="Empty Org")   # zero members
    rollup = {o["org"].name: o for o in services.managed_organisations()}
    assert rollup["Riverside Council"]["learners"] == 1     # Sam
    assert rollup["Empty Org"]["learners"] == 0             # still listed
    assert "Empty Org" in rollup


def test_organisation_members_lists_only_that_org(world):
    from staff import services

    members = services.organisation_members(world["council"])
    assert {r.user.email for r in members} == {"sam@example.com"}


# --- Empty state + page rendering ------------------------------------------

def test_organisations_page_with_no_orgs_shows_the_no_org_group(client, db):
    # No organisations, but the admin themselves is unassigned → the page shows
    # the No-organisation group rather than crashing or hiding everyone.
    admin = make_user("solo@example.com", "Solo", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])
    client.force_login(admin)
    body = client.get(reverse("staff:organisations")).content.decode()
    assert "No organisation" in body
    assert reverse("staff:unassigned") in body


def test_org_detail_lists_members(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:org_detail", args=[world["council"].pk])).content.decode()
    assert "Sam" in body
    assert "sam@example.com" in body


# --- Add-user routes org through the resolver ------------------------------

def test_add_user_creates_managed_organisation(client, world):
    as_admin(client, world)
    client.post(reverse("staff:user_new"), {
        "first_name": "Liam", "last_name": "Ng", "email": "liam@council.gov.au",
        "role": User.Role.STUDENT, "organisation": "Barwon Health",
        "password": "three-random-words-xyz",
    })
    liam = User.objects.get(email="liam@council.gov.au")
    org = Organisation.objects.get(name="Barwon Health")
    assert liam.profile.org_id == org.pk
    assert liam.profile.organisation == "Barwon Health"


# --- Navigation tidy -------------------------------------------------------

def test_django_admin_is_demoted_to_the_sidebar_foot(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:overview")).content.decode()
    # The raw Django admin is no longer a peer nav item; it sits in the foot.
    assert "cy-side__adv" in body
    assert "Raw data" in body
    # Exactly one link to /admin/ (the de-emphasised one), not a nav item too.
    assert body.count(reverse("admin:index")) == 1


# --- Delete organisation ---------------------------------------------------

def test_delete_org_detaches_members_and_audits(client, world):
    as_admin(client, world)
    council = world["council"]
    resp = client.post(reverse("staff:org_delete", args=[council.pk]))
    assert resp.status_code == 302 and resp.url == reverse("staff:organisations")
    assert not Organisation.objects.filter(pk=council.pk).exists()
    # Sam is kept, but detached (FK cleared AND text mirror blanked).
    world["sam"].refresh_from_db()
    profile = world["sam"].profile
    profile.refresh_from_db()
    assert User.objects.filter(pk=world["sam"].pk).exists()
    assert profile.org is None and profile.organisation == ""
    assert AdminAction.objects.filter(action=AdminAction.Kind.DELETE_ORG).exists()


def test_delete_org_is_admin_only(client, world):
    client.force_login(world["sam"])
    assert client.post(reverse("staff:org_delete", args=[world["council"].pk])).status_code == 403
    assert Organisation.objects.filter(pk=world["council"].pk).exists()


# --- Send a note to an organisation ----------------------------------------

def test_send_note_to_org_emails_members_and_audits(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:send_note_org", args=[world["council"].pk]),
                       {"message": "Well done this week, keep it up."})
    assert resp.status_code == 302
    # One member (Sam) → one email, carrying the note.
    assert len(mail.outbox) == 1
    assert world["sam"].email in mail.outbox[0].to
    assert "keep it up" in mail.outbox[0].body
    assert AdminAction.objects.filter(action=AdminAction.Kind.NOTE_ORG).exists()


def test_send_note_to_org_rejects_empty(client, world):
    as_admin(client, world)
    client.post(reverse("staff:send_note_org", args=[world["council"].pk]), {"message": "  "})
    assert len(mail.outbox) == 0
    assert not AdminAction.objects.filter(action=AdminAction.Kind.NOTE_ORG).exists()


def test_send_note_to_org_is_admin_only(client, world):
    client.force_login(world["sam"])
    assert client.post(reverse("staff:send_note_org", args=[world["council"].pk]),
                       {"message": "hi"}).status_code == 403


# --- Send a note to an individual ------------------------------------------

def test_send_note_to_user_emails_and_audits(client, world):
    as_admin(client, world)
    resp = client.post(reverse("staff:send_note_user", args=[world["sam"].pk]),
                       {"message": "A quick personal note."})
    assert resp.status_code == 302
    assert len(mail.outbox) == 1
    assert world["sam"].email in mail.outbox[0].to
    assert AdminAction.objects.filter(
        action=AdminAction.Kind.NOTE_USER, target_user=world["sam"]
    ).exists()


def test_send_note_to_user_is_admin_only(client, world):
    client.force_login(world["sam"])
    assert client.post(reverse("staff:send_note_user", args=[world["sam"].pk]),
                       {"message": "hi"}).status_code == 403


# --- No-organisation group -------------------------------------------------

def test_unassigned_lists_people_with_no_org(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:unassigned")).content.decode()
    assert "dana@example.com" in body        # unassigned
    assert "sam@example.com" not in body      # in an org


def test_unassigned_is_admin_only(client, world):
    client.force_login(world["sam"])
    assert client.get(reverse("staff:unassigned")).status_code == 403


def test_org_list_shows_no_organisation_group(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:organisations")).content.decode()
    assert "No organisation" in body
    assert reverse("staff:unassigned") in body
