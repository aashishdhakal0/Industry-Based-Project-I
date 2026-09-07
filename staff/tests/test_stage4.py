"""Stage 4 — reporting & compliance hub, due dates, certificate register.

The as-at-a-date cutoff, the compliance summary (with an organisation's due
date), the certificate register + revoke/reinstate, CSV exports, and access
control on all of it.
"""

import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import Organisation, User, UserProfile
from certificates.models import Certificate
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult
from staff import services
from staff.models import AdminAction

PASSWORD = "correct-horse-battery"


def mkstudent(email, first, org=None):
    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Lee",
        role=User.Role.STUDENT, is_verified=True,
    )
    p = UserProfile.objects.create(user=u)
    if org:
        services.assign_learner_org(p, org)
    return u


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)
    module = Module.objects.create(title="Module 1", order_index=1,
                                   is_published=True, created_by=admin)
    lesson = Lesson.objects.create(module=module, lesson_number=1, title="L1")
    quiz = Quiz.objects.create(module=module, is_active=True, pass_mark=70)
    return {"admin": admin, "module": module, "lesson": lesson, "quiz": quiz}


def complete_course(world, learner, when):
    """Complete the one module and backdate the records to `when`."""
    ProgressRecord.objects.create(user=learner, lesson=world["lesson"])
    QuizResult.objects.create(user=learner, quiz=world["quiz"], score=90,
                              passed=True, attempt_number=1)
    aware = timezone.make_aware(datetime.datetime.combine(when, datetime.time(12, 0)))
    ProgressRecord.objects.filter(user=learner).update(completed_at=aware)
    QuizResult.objects.filter(user=learner).update(submitted_at=aware)


# --- as-at-a-date cutoff -----------------------------------------------------


def test_collect_as_at_reflects_only_records_up_to_that_date(world):
    alice = mkstudent("alice@example.com", "Alice")
    complete_course(world, alice, datetime.date(2026, 6, 15))

    def done_as_at(d):
        aware = timezone.make_aware(datetime.datetime.combine(d, datetime.time.max))
        rows = {r.user.email: r for r in services.collect_learners(as_at=aware)}
        return rows["alice@example.com"].completed_course

    assert done_as_at(datetime.date(2026, 6, 14)) is False   # before she finished
    assert done_as_at(datetime.date(2026, 6, 16)) is True     # after


# --- compliance report -------------------------------------------------------


def test_compliance_summary_counts(world):
    a = mkstudent("a@example.com", "A")
    complete_course(world, a, datetime.date(2026, 6, 1))
    mkstudent("b@example.com", "B")   # never started

    report = services.compliance_report()
    assert report["total"] == 2
    assert report["completed"] == 1
    assert report["not_completed"] == 1
    assert report["rate"] == 50


def test_compliance_scoped_to_org_with_due_date(world):
    org = Organisation.objects.create(
        name="Bendigo Council", training_due=datetime.date(2020, 1, 1)  # long past
    )
    inside = mkstudent("inside@example.com", "In", org=org)
    mkstudent("outside@example.com", "Out")   # different (no) org

    report = services.compliance_report(org=org)
    assert report["total"] == 1                       # only the org member
    assert report["rows"][0].user == inside
    assert report["due"] == datetime.date(2020, 1, 1)
    assert report["past_due"] is True                 # due date has passed


def test_compliance_csv_export(client, world):
    a = mkstudent("a@example.com", "A")
    complete_course(world, a, datetime.date(2026, 6, 1))
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:report_compliance") + "?format=csv")
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    body = resp.content.decode()
    assert "Completed course" in body
    assert "a@example.com" in body


# --- certificate register ----------------------------------------------------


def test_certificate_register_filters_by_status(world):
    a = mkstudent("a@example.com", "A")
    b = mkstudent("b@example.com", "B")
    Certificate.objects.create(user=a, grade="Distinction")
    revoked = Certificate.objects.create(user=b, grade="Merit")
    revoked.revoked_at = timezone.now()
    revoked.save(update_fields=["revoked_at"])

    assert len(services.certificate_register()) == 2
    assert len(services.certificate_register(status="valid")) == 1
    assert len(services.certificate_register(status="revoked")) == 1


def test_revoke_then_reinstate_certificate_audits_both(client, world):
    a = mkstudent("a@example.com", "A")
    cert = Certificate.objects.create(user=a, grade="Distinction")
    client.force_login(world["admin"])

    client.post(reverse("staff:revoke_cert", args=[cert.pk]))
    cert.refresh_from_db()
    assert cert.revoked_at is not None
    assert AdminAction.objects.filter(action=AdminAction.Kind.REVOKE_CERT).count() == 1

    client.post(reverse("staff:revoke_cert", args=[cert.pk]))   # toggle back
    cert.refresh_from_db()
    assert cert.revoked_at is None
    assert AdminAction.objects.filter(action=AdminAction.Kind.REVOKE_CERT).count() == 2


def test_certificate_register_csv(client, world):
    a = mkstudent("a@example.com", "A")
    Certificate.objects.create(user=a, grade="Distinction")
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:certificate_register") + "?format=csv")
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    body = resp.content.decode()
    assert "Serial,Holder" in body
    assert "a@example.com" in body


# --- due date on the organisation form --------------------------------------


def test_overdue_org_is_flagged_on_list_and_detail(client, world):
    org = Organisation.objects.create(
        name="Riverside Dental", training_due=datetime.date(2020, 1, 1)  # long past
    )
    mkstudent("behind@example.com", "Behind", org=org)  # not complete
    client.force_login(world["admin"])

    listing = client.get(reverse("staff:organisations")).content.decode()
    assert "Overdue" in listing
    detail = client.get(reverse("staff:org_detail", args=[org.pk])).content.decode()
    assert "Overdue" in detail
    assert "Compliance report" in detail


def test_org_not_overdue_when_everyone_complete(client, world):
    org = Organisation.objects.create(
        name="Kensington Physio", training_due=datetime.date(2020, 1, 1)
    )
    done = mkstudent("done@example.com", "Done", org=org)
    complete_course(world, done, datetime.date(2019, 6, 1))
    rows = {o["org"].pk: o for o in services.managed_organisations()}
    assert rows[org.pk]["overdue"] is False


def test_org_form_saves_training_due(client, world):
    org = Organisation.objects.create(name="Yarra Freight")
    client.force_login(world["admin"])
    client.post(reverse("staff:org_detail", args=[org.pk]),
               {"name": "Yarra Freight", "training_due": "2026-12-31"})
    org.refresh_from_db()
    assert org.training_due == datetime.date(2026, 12, 31)


# --- access control ----------------------------------------------------------


@pytest.mark.parametrize("name", [
    "staff:reports", "staff:report_compliance", "staff:certificate_register",
])
def test_report_pages_are_admin_only(client, world, name):
    student = mkstudent("s@example.com", "S")
    client.force_login(student)
    assert client.get(reverse(name)).status_code == 403


def test_revoke_is_admin_only_and_post_only(client, world):
    a = mkstudent("a@example.com", "A")
    cert = Certificate.objects.create(user=a, grade="Merit")
    client.force_login(a)
    assert client.post(reverse("staff:revoke_cert", args=[cert.pk])).status_code == 403
    client.force_login(world["admin"])
    assert client.get(reverse("staff:revoke_cert", args=[cert.pk])).status_code == 405
