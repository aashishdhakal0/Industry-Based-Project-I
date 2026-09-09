"""Stage 1 — overview command centre (trends + attention cohorts) and the
filterable, searchable, exportable audit log.

Covers the new aggregates, the four cohorts, the new quick-filters, and the
audit-log filtering + CSV, including access control and that filtering never
leaks past the administrator gate.
"""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult
from staff import services
from staff.models import AdminAction

PASSWORD = "correct-horse-battery"


def student(email, first, *, verified=True, points=0, days_ago=None):
    u = User.objects.create_user(
        email=email, password=PASSWORD, first_name=first, last_name="Test",
        role=User.Role.STUDENT, is_verified=verified,
    )
    last = timezone.now() - timedelta(days=days_ago) if days_ago is not None else None
    UserProfile.objects.create(user=u, points=points, last_active=last)
    return u


@pytest.fixture
def world(db):
    admin = User.objects.create_user(
        email="admin@example.com", password=PASSWORD, first_name="Ada",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=admin)

    modules = {}
    for i in (1, 2):
        m = Module.objects.create(title=f"Module {i}", order_index=i,
                                  is_published=True, created_by=admin)
        for n in (1, 2):
            Lesson.objects.create(module=m, lesson_number=n, title=f"L{n}")
        m.quiz_obj = Quiz.objects.create(module=m, is_active=True, pass_mark=70)
        modules[i] = m

    # carol: verified, nothing done -> not_started
    carol = student("carol@example.com", "Carol")

    # stan: started module 1, then quiet 20 days -> stalled mid-course
    stan = student("stan@example.com", "Stan", points=100, days_ago=20)
    for lesson in modules[1].lessons.all():
        ProgressRecord.objects.create(user=stan, lesson=lesson)

    # val: never confirmed email -> awaiting verification
    val = student("val@example.com", "Val", verified=False)

    # rey: two failed attempts on module 1, never passed -> repeat quiz-failer
    rey = student("rey@example.com", "Rey", points=50, days_ago=2)
    QuizResult.objects.create(user=rey, quiz=modules[1].quiz_obj, score=50,
                              passed=False, attempt_number=1)
    QuizResult.objects.create(user=rey, quiz=modules[1].quiz_obj, score=60,
                              passed=False, attempt_number=2)

    return {"admin": admin, "modules": modules,
            "carol": carol, "stan": stan, "val": val, "rey": rey}


# --- repeat-fail flag + cohorts ---------------------------------------------


def test_repeat_failed_flag_is_computed(world):
    by_email = {r.user.email: r for r in services.collect_learners()}
    assert by_email["rey@example.com"].repeat_failed is True
    # a learner who passed, or never attempted, is not a repeat-failer
    assert by_email["carol@example.com"].repeat_failed is False
    assert by_email["stan@example.com"].repeat_failed is False


def test_a_single_fail_is_not_a_repeat_failer(world):
    # one failed attempt is not "repeatedly failing"
    QuizResult.objects.filter(user=world["rey"]).exclude(attempt_number=1).delete()
    by_email = {r.user.email: r for r in services.collect_learners()}
    assert by_email["rey@example.com"].repeat_failed is False


def test_passing_clears_the_repeat_fail_flag(world):
    QuizResult.objects.create(user=world["rey"], quiz=world["modules"][1].quiz_obj,
                              score=90, passed=True, attempt_number=3)
    by_email = {r.user.email: r for r in services.collect_learners()}
    assert by_email["rey@example.com"].repeat_failed is False


def test_attention_cohorts_group_the_right_people(world):
    cohorts = {c["key"]: c for c in services.attention_cohorts(services.collect_learners())}
    assert set(cohorts) == {"not_started", "stalled", "repeat_failed", "unverified"}
    # not_started includes carol AND val (val is verified=False but also unstarted)
    names = {c: {r.user.email for r in cohorts[c]["sample"]} for c in cohorts}
    assert "carol@example.com" in names["not_started"]
    assert names["stalled"] == {"stan@example.com"}
    assert names["repeat_failed"] == {"rey@example.com"}
    assert names["unverified"] == {"val@example.com"}


def test_cohort_counts_match_samples(world):
    for c in services.attention_cohorts(services.collect_learners(), sample=1):
        assert c["count"] >= len(c["sample"])
        assert c["more"] == max(0, c["count"] - len(c["sample"]))


# --- period metrics ----------------------------------------------------------


def test_period_metrics_shape_and_movement(world):
    p = services.period_metrics()
    assert p["days"] == 7
    assert len(p["metrics"]) == 3
    for m in p["metrics"]:
        assert {"label", "current", "previous", "delta"} <= set(m)
        assert m["delta"] == m["current"] - m["previous"]
    # stan's two lesson completions landed just now -> events this period
    assert p["events"]["current"] >= 2


# --- new quick-filters on the learners page ---------------------------------


@pytest.mark.parametrize(
    "key,present,absent",
    [
        ("stalled", "stan@example.com", "carol@example.com"),
        ("repeat_failed", "rey@example.com", "stan@example.com"),
        ("unverified", "val@example.com", "carol@example.com"),
    ],
)
def test_new_quick_filters_narrow_the_list(client, world, key, present, absent):
    client.force_login(world["admin"])
    body = client.get(
        reverse("staff:learners") + f"?view=list&filter={key}"
    ).content.decode()
    assert present in body
    assert absent not in body


def test_status_filter_uses_new_param(client, world):
    """The status axis reads from ?status= (the dropdown/chip param)."""
    client.force_login(world["admin"])
    body = client.get(
        reverse("staff:learners") + "?view=list&status=stalled"
    ).content.decode()
    assert "stan@example.com" in body
    assert "carol@example.com" not in body


def test_status_and_grade_are_independent_and_combine(client, world):
    """Status and grade are two filters applied together, not one exclusive pick."""
    client.force_login(world["admin"])
    # rey is a repeat-failer whose grade is Not yet (two failed attempts).
    both = client.get(
        reverse("staff:learners") + "?view=list&status=repeat_failed&grade=not-yet"
    ).content.decode()
    assert "rey@example.com" in both
    # The same status with a grade rey does NOT hold excludes him.
    narrowed = client.get(
        reverse("staff:learners") + "?view=list&status=repeat_failed&grade=distinction"
    ).content.decode()
    assert "rey@example.com" not in narrowed


def test_legacy_filter_param_still_maps(client, world):
    """Old ?filter= links (grade or status) keep working after the split."""
    client.force_login(world["admin"])
    ctx = client.get(reverse("staff:learners") + "?view=list&filter=unverified")
    assert ctx.context["status"] == "unverified" and ctx.context["grade"] == ""
    ctx2 = client.get(reverse("staff:learners") + "?view=list&filter=distinction")
    assert ctx2.context["grade"] == "distinction" and ctx2.context["status"] == ""


# --- overview page renders the new sections ---------------------------------


def test_overview_shows_activity_and_consolidated_attention(client, world):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:overview")).content.decode()
    # Completion-led hero + the two charts + the consolidated attention section.
    assert "Training completion" in body
    assert "Activity over time" in body
    assert "Grade distribution" in body
    assert "Needs attention" in body
    assert "cy-c-attchip" in body               # the four category chips, consolidated
    assert "cy-c-chart" in body                 # the activity area chart (world has activity)


# --- audit log: filtering, search, CSV, access control ----------------------


@pytest.fixture
def logged(world):
    """Seed a spread of audit actions by two different administrators."""
    ada = world["admin"]
    ben = User.objects.create_user(
        email="ben@example.com", password=PASSWORD, first_name="Ben",
        role=User.Role.ADMINISTRATOR, is_staff=True, is_verified=True,
    )
    UserProfile.objects.create(user=ben)
    services.log_action(ada, AdminAction.Kind.NUDGE,
                        "Sent a nudge to carol@example.com", target_user=world["carol"])
    services.log_action(ben, AdminAction.Kind.DEACTIVATE,
                        "Deactivated stan@example.com", target_user=world["stan"])
    services.log_action(ada, AdminAction.Kind.CREATE_ORG, "Created organisation “Acme”")
    return {"ada": ada, "ben": ben}


# NB: the filter bar's Action dropdown contains the short kind labels
# ("Sent a nudge"), so assertions target the full summary strings (which carry
# the email and never appear in a dropdown option) to prove the FEED narrowed.


def test_activity_filters_by_actor(client, world, logged):
    client.force_login(world["admin"])
    body = client.get(
        reverse("staff:activity") + f"?actor={logged['ben'].pk}"
    ).content.decode()
    assert "Deactivated stan@example.com" in body
    assert "Sent a nudge to carol@example.com" not in body


def test_activity_filters_by_kind(client, world, logged):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:activity") + "?kind=nudge").content.decode()
    assert "Sent a nudge to carol@example.com" in body
    assert "Deactivated stan@example.com" not in body


def test_activity_free_text_search(client, world, logged):
    client.force_login(world["admin"])
    body = client.get(reverse("staff:activity") + "?q=Acme").content.decode()
    assert "Created organisation" in body
    assert "Sent a nudge to carol@example.com" not in body


def test_activity_date_range_filters(client, world, logged):
    client.force_login(world["admin"])
    tomorrow = (timezone.localdate() + timedelta(days=1)).isoformat()
    # everything is "today", so a from=tomorrow window is empty
    body = client.get(reverse("staff:activity") + f"?from={tomorrow}").content.decode()
    assert "No actions match these filters" in body


def test_activity_bad_date_is_ignored_not_500(client, world, logged):
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:activity") + "?from=not-a-date")
    assert resp.status_code == 200
    assert "Sent a nudge" in resp.content.decode()


def test_activity_csv_exports_filtered_rows(client, world, logged):
    client.force_login(world["admin"])
    resp = client.get(reverse("staff:activity_csv") + "?kind=nudge")
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    body = resp.content.decode()
    assert "When,Administrator,Action,Affected account,Detail" in body
    assert "Sent a nudge to carol@example.com" in body
    assert "Deactivated" not in body      # the kind filter carried into the export


@pytest.mark.parametrize("name", ["staff:activity", "staff:activity_csv"])
def test_activity_is_admin_only(client, world, name):
    client.force_login(world["carol"])          # a student
    assert client.get(reverse(name)).status_code == 403


@pytest.mark.parametrize("name", ["staff:activity", "staff:activity_csv"])
def test_activity_sends_anonymous_to_login(client, world, name):
    resp = client.get(reverse(name))
    assert resp.status_code == 302
    assert reverse("authentication:login") in resp.url
