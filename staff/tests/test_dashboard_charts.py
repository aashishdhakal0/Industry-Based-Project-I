"""The chart-driven overview: real weekly trends, hand-built SVG geometry, the
module-completion funnel, the grade donut, and the per-organisation CSV.

Geometry is computed server-side, so it is unit-tested directly; the page then
just drops it into SVG. Empty/sparse data must degrade gracefully.
"""

import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from authentication.models import Organisation, User, UserProfile
from modules.models import Lesson, Module, ProgressRecord
from quizzes.models import Quiz, QuizResult

PASSWORD = "correct-horse-battery"
REF = datetime.date(2026, 8, 11)          # a Tuesday; its Monday is 2026-08-10


def _aware(d, hour=12):
    return timezone.make_aware(datetime.datetime.combine(d, datetime.time(hour, 0)))


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

    return {"admin": admin, "module": module, "quiz": quiz, "org": org, "finn": finn}


def as_admin(client, world):
    client.force_login(world["admin"])


# --- Pure geometry (deterministic) -----------------------------------------

def test_sparkline_normalises_and_flags_flat():
    from staff import services

    sp = services.sparkline([1, 3, 2, 5])
    assert not sp.flat and sp.line and sp.area
    assert services.sparkline([]).flat is True
    assert services.sparkline([4, 4, 4]).flat is True     # no range → flat


def test_donut_arcs_sum_to_the_circumference():
    from staff import services

    d = services.donut([("distinction", "Distinction", 3), ("pass", "Pass", 1)])
    assert d.total == 4
    assert [s.percent for s in d.segments] == [75, 25]
    assert round(sum(s.dash for s in d.segments), 2) == round(d.circumference, 2)
    assert services.donut([("x", "X", 0)]).empty is True


def test_area_chart_is_empty_when_nothing_to_plot():
    from staff import services

    assert services.area_chart([0, 0, 0], ["a", "b", "c"]).empty is True
    c = services.area_chart([1, 4, 2], ["a", "b", "c"])
    assert not c.empty and c.max_value >= 4 and c.line


# --- Real weekly trends (bounded) ------------------------------------------

def test_weekly_completions_bucket_by_week(world):
    from staff import services

    # Two lessons completed this week, one last week.
    prs = list(ProgressRecord.objects.filter(user=world["finn"]))
    ProgressRecord.objects.filter(pk=prs[0].pk).update(completed_at=_aware(REF))              # this week
    ProgressRecord.objects.filter(pk=prs[1].pk).update(completed_at=_aware(REF - datetime.timedelta(days=7)))  # last week
    # The quiz pass counts as a completion too — put it this week.
    QuizResult.objects.filter(user=world["finn"]).update(submitted_at=_aware(REF))

    trends = services.weekly_trends(weeks=4, now=REF)
    assert len(trends["completions"]) == 4
    assert trends["completions"][-1] == 2      # 1 lesson + 1 quiz pass this week
    assert trends["completions"][-2] == 1      # 1 lesson last week


def test_weekly_signups_are_cumulative(world):
    from staff import services

    trends = services.weekly_trends(weeks=4, now=REF)
    # One student total; the cumulative line never exceeds the learner count.
    assert trends["signups"][-1] == 1
    assert trends["signups"] == sorted(trends["signups"])   # monotonic non-decreasing


# --- Module funnel ---------------------------------------------------------

def test_module_funnel_counts_completions(world):
    from staff import services

    funnel = services.module_funnel()
    assert len(funnel) == 1
    row = funnel[0]
    assert row["module"] == world["module"]
    assert row["completed"] == 1 and row["total"] == 1 and row["percent"] == 100


# --- overview_charts bundle ------------------------------------------------

def test_overview_charts_bundle_has_every_piece(world):
    from staff import services

    stats = services.overview(services.collect_learners())
    charts = services.overview_charts(stats)
    for key in ("spark_learners", "spark_active", "spark_completions", "spark_avg",
                "completions_chart", "grade_donut", "funnel", "active_now"):
        assert key in charts
    # Finn is a distinction → the donut has a distinction segment.
    slugs = [s.slug for s in charts["grade_donut"].segments]
    assert "distinction" in slugs


# --- Page render + graceful empties ----------------------------------------

def test_overview_renders_the_charts(client, world):
    as_admin(client, world)
    body = client.get(reverse("staff:overview")).content.decode()
    assert "cy-c-kpis--spark" in body      # KPI sparkline cards
    assert "cy-spark__line" in body
    assert "cy-area" in body               # main completions chart
    assert "cy-donut" in body              # grade donut
    assert "cy-c-funnel__fill" in body     # module funnel
    assert "Completions over time" in body


def test_overview_survives_a_learner_with_no_activity(client, db):
    """Sparse data must not crash: flat sparklines, empty area/donut states."""
    admin = make_user("solo@example.com", "Solo", role=User.Role.ADMINISTRATOR)
    admin.is_staff = True
    admin.save(update_fields=["is_staff"])
    make_user("newbie@example.com", "New")   # a learner, no activity
    client.force_login(admin)
    resp = client.get(reverse("staff:overview"))
    assert resp.status_code == 200
    assert "No completions yet" in resp.content.decode()   # area chart empty state


# --- Per-organisation CSV --------------------------------------------------

def test_org_csv_exports_that_orgs_members(client, world):
    as_admin(client, world)
    resp = client.get(reverse("staff:org_learners_csv", args=[world["org"].pk]))
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    assert "riverside-council" in resp["Content-Disposition"]
    text = resp.content.decode()
    assert "finn@example.com" in text
    assert "Distinction" in text


def test_org_csv_is_admin_only(client, world):
    client.force_login(world["finn"])
    assert client.get(reverse("staff:org_learners_csv", args=[world["org"].pk])).status_code == 403
    client.logout()
    resp = client.get(reverse("staff:org_learners_csv", args=[world["org"].pk]))
    assert resp.status_code == 302 and reverse("authentication:login") in resp.url
