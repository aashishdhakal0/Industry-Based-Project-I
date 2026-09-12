"""The student-facing views: browser, overview, lesson, completion, simulation.

The load-bearing assertions are the lock (a real 403 from the view, not a hidden
link) and that completion awards real points once.
"""

import json

import pytest
from django.urls import reverse

from modules.models import ProgressRecord, SimulationResult


@pytest.fixture
def client_student(client, student):
    client.force_login(student)
    return client


def complete(client, module, lesson_number, **extra):
    return client.post(
        reverse("learn:complete_lesson", args=[module.order_index, lesson_number]),
        **extra,
    )


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_the_whole_learn_area_requires_login(client, modules):
    for name, args in [
        ("learn:browser", []),
        ("learn:module", [1]),
        ("learn:lesson", [1, 1]),
        ("learn:simulation", [1]),
    ]:
        response = client.get(reverse(name, args=args))
        assert response.status_code == 302
        assert "/login/" in response.url, name


# --------------------------------------------------------------------------
# Browser + overview
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_browser_lists_the_published_modules(client_student, modules):
    html = client_student.get(reverse("learn:browser")).content.decode()
    for m in modules:
        assert m.title in html


@pytest.mark.django_db
def test_overview_of_the_first_module_is_reachable(client_student, modules):
    assert client_student.get(reverse("learn:module", args=[1])).status_code == 200


# --------------------------------------------------------------------------
# The lock — enforced in the view, not just hidden
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_locked_module_overview_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:module", args=[2])).status_code == 403


@pytest.mark.django_db
def test_a_locked_module_lesson_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:lesson", args=[2, 1])).status_code == 403


@pytest.mark.django_db
def test_a_locked_module_simulation_returns_403(client_student, modules):
    assert client_student.get(reverse("learn:simulation", args=[2])).status_code == 403


@pytest.mark.django_db
def test_finishing_a_module_unlocks_the_next_overview(client_student, modules):
    for n in range(1, 5):
        complete(client_student, modules[0], n)
    assert client_student.get(reverse("learn:module", args=[2])).status_code == 200


# --------------------------------------------------------------------------
# Lesson + completion
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_lesson_renders_its_body(client_student, modules):
    response = client_student.get(reverse("learn:lesson", args=[1, 1]))
    assert response.status_code == 200
    assert b"Placeholder" in response.content


@pytest.mark.django_db
def test_marking_complete_records_progress_and_awards_points(client_student, student, modules):
    response = complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    data = json.loads(response.content)

    assert data["points_gained"] == 50
    assert data["points"] == 50
    assert ProgressRecord.objects.filter(user=student, lesson__module=modules[0]).count() == 1


@pytest.mark.django_db
def test_marking_complete_twice_awards_once(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    second = complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    data = json.loads(second.content)

    assert data["points_gained"] == 0
    assert data["points"] == 50
    assert ProgressRecord.objects.filter(user=student).count() == 1


@pytest.mark.django_db
def test_completion_without_js_redirects_to_the_next_lesson(client_student, modules):
    response = complete(client_student, modules[0], 1)
    assert response.status_code == 302
    assert response.url == reverse("learn:lesson", args=[1, 2])


@pytest.mark.django_db
def test_finishing_the_last_lesson_of_a_quizless_module_returns_to_the_module(
    client_student, modules
):
    # These fixture modules have no quiz, so the last lesson completes the module
    # and the student is sent back to its (now complete) overview — never stranded.
    for n in range(1, 4):
        complete(client_student, modules[0], n)
    last = complete(client_student, modules[0], 4)
    assert last.status_code == 302
    assert last.url == reverse("learn:module", args=[1])


@pytest.mark.django_db
def test_last_lesson_completion_reports_the_module_as_done(client_student, modules):
    for n in range(1, 4):
        complete(client_student, modules[0], n, HTTP_X_REQUESTED_WITH="fetch")
    data = json.loads(
        complete(client_student, modules[0], 4, HTTP_X_REQUESTED_WITH="fetch").content
    )
    assert data["module_done"] is True
    assert data["next_url"] == reverse("learn:module", args=[1])


@pytest.mark.django_db
def test_an_unfinished_module_overview_shows_no_completion_card(client_student, modules):
    complete(client_student, modules[0], 1)
    html = client_student.get(reverse("learn:module", args=[1])).content.decode()
    assert "cy-moddone" not in html


@pytest.mark.django_db
def test_a_completed_module_overview_celebrates_and_offers_the_next_module(
    client_student, modules
):
    for n in range(1, 5):
        complete(client_student, modules[0], n)
    html = client_student.get(reverse("learn:module", args=[1])).content.decode()
    assert "cy-moddone" in html                       # the celebration card
    assert "Module 01 complete" in html
    assert "XP earned" in html
    assert "is now unlocked" in html
    # A prominent way forward to the next module.
    assert "Start Module 2" in html
    assert reverse("learn:module", args=[2]) in html
    # No unrendered template tokens leaking into the finished-module view.
    for token in ("{{", "{%", "{#"):
        assert token not in html


@pytest.mark.django_db
def test_the_final_module_completion_points_to_the_certificate(client_student, modules):
    # Complete all three fixture modules (quizless, so lessons-only), unlocking
    # each in turn; the last one has no next module, so it offers the certificate.
    for module in modules:
        for n in range(1, 5):
            complete(client_student, module, n)
    html = client_student.get(reverse("learn:module", args=[3])).content.decode()
    assert "cy-moddone" in html
    assert "See your certificate" in html
    assert reverse("learn:certificate") in html
    assert "Start Module" not in html


@pytest.mark.django_db
def test_completion_is_post_only(client_student, modules):
    url = reverse("learn:complete_lesson", args=[1, 1])
    assert client_student.get(url).status_code == 405


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_simulation_page_renders_with_the_scenario_data(client_student, modules):
    response = client_student.get(reverse("learn:simulation", args=[1]))
    assert response.status_code == 200
    assert b'id="cy-sim-data"' in response.content


@pytest.mark.django_db
def test_completing_a_simulation_stores_the_result(client_student, student, modules):
    response = client_student.post(
        reverse("learn:complete_simulation", args=[1]),
        data=json.dumps({"score": 1, "total": 1, "path": [{"id": "a", "correct": True}]}),
        content_type="application/json",
    )
    assert response.status_code == 200
    result = SimulationResult.objects.get(user=student, simulation=modules[0].simulation)
    assert result.score == 1
    assert result.total == 1


@pytest.mark.django_db
def test_a_tampered_simulation_score_is_clamped(client_student, student, modules):
    """A client posting score 99 out of 1 shouldn't be believed."""
    client_student.post(
        reverse("learn:complete_simulation", args=[1]),
        data=json.dumps({"score": 99, "total": 1, "path": []}),
        content_type="application/json",
    )
    result = SimulationResult.objects.get(user=student)
    assert result.score == 1  # clamped to total


@pytest.mark.django_db
def test_browser_query_count_is_bounded(client_student, make_module, django_assert_max_num_queries):
    for i in range(1, 7):
        make_module(i)
    # Whatever the fixed cost is, it must not grow with module count. Generous
    # ceiling: auth, session, profile, and the progress queries (module_progress
    # now runs four — lessons, lesson-progress, gated-module set, passed-quiz set
    # — and the view resolves it more than once). Six modules seeded; the point
    # of the test is that this stays flat, not that it's minimal.
    with django_assert_max_num_queries(18):
        client_student.get(reverse("learn:browser"))


# --------------------------------------------------------------------------
# Dashboard — real data from the database
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_shows_real_points_after_completing_lessons(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    complete(client_student, modules[0], 2, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    # 2 lessons × 50 = 100 points, shown in the points stat card.
    assert 'cy-stat__v">100<' in html


@pytest.mark.django_db
def test_dashboard_reflects_earned_badges(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    # The badges stat reflects the one just earned and links to the gallery.
    assert reverse("learn:badges") in html
    assert "1 <small>/ 11</small>" in html


@pytest.mark.django_db
def test_dashboard_continue_points_at_the_next_lesson(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert reverse("learn:module", args=[1]) in html
    assert "Continue learning" in html


# --------------------------------------------------------------------------
# Rendering hygiene — no template leaks, no emoji, on the new pages
# --------------------------------------------------------------------------

import re

LEAKS = ["{#", "#}", "{%", "%}", "{{", "}}"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


@pytest.mark.django_db
def test_learn_pages_render_clean_and_without_emoji(client_student, modules):
    urls = [
        reverse("learn:browser"),
        reverse("learn:module", args=[1]),
        reverse("learn:lesson", args=[1, 1]),
        reverse("learn:simulation", args=[1]),
        reverse("learn:progress"),
        reverse("learn:badges"),
        reverse("learn:certificate"),
        reverse("dashboard"),
    ]
    for url in urls:
        html = client_student.get(url).content.decode()
        for token in LEAKS:
            assert token not in html, f"{url} leaked {token!r}"
        assert not EMOJI.findall(html), f"{url} contains emoji"


# --------------------------------------------------------------------------
# The app shell — sidebar, active state, new pages
# --------------------------------------------------------------------------

# The sidebar-shell pages. The lesson is deliberately excluded: it renders the
# focused, distraction-free room shell (no sidebar) tested separately below.
STUDENT_PATHS = [
    ("learn:browser", []),
    ("dashboard", []),
    ("learn:progress", []),
    ("learn:badges", []),
    ("learn:certificate", []),
    ("learn:module", [1]),
    ("learn:simulation", [1]),
]


@pytest.mark.django_db
def test_every_student_page_lives_in_the_app_shell(client_student, modules):
    for name, args in STUDENT_PATHS:
        html = client_student.get(reverse(name, args=args)).content.decode()
        assert 'class="cy-side__nav"' in html, name
        # the mobile drawer toggle, wired to the sidebar
        assert 'aria-controls="cy-side"' in html, name


@pytest.mark.django_db
def test_a_lesson_uses_the_focused_room_shell(client_student, modules):
    """In a lesson the sidebar drops away for a distraction-free room, with a
    slim focus bar and a clear way back to the module."""
    html = client_student.get(reverse("learn:lesson", args=[1, 1])).content.decode()
    assert "cy-app--focus" in html
    assert "cy-focusbar__back" in html
    assert reverse("learn:module", args=[1]) in html      # back to the module
    assert 'class="cy-side__nav"' not in html             # no sidebar to distract


@pytest.mark.django_db
def test_sidebar_links_to_every_section(client_student, modules):
    html = client_student.get(reverse("dashboard")).content.decode()
    for name in ["dashboard", "learn:browser", "learn:progress", "learn:badges", "learn:certificate"]:
        assert reverse(name) in html


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name,active_key",
    [("dashboard", "Dashboard"), ("learn:progress", "My progress"), ("learn:badges", "Badges")],
)
def test_the_right_sidebar_item_is_active(client_student, modules, name, active_key):
    html = client_student.get(reverse(name)).content.decode()
    # the active item and its label appear together
    marker = 'cy-side__item is-active'
    assert marker in html
    idx = html.index(marker)
    assert active_key in html[idx : idx + 200]


@pytest.mark.django_db
def test_new_pages_show_real_data(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    progress = client_student.get(reverse("learn:progress")).content.decode()
    assert modules[0].title in progress

    badges = client_student.get(reverse("learn:badges")).content.decode()
    assert "First step" in badges and "cy-collect is-earned" in badges

    cert = client_student.get(reverse("learn:certificate")).content.decode()
    assert "certificate" in cert.lower()


@pytest.mark.django_db
def test_new_pages_require_login(client, modules):
    for name in ["learn:progress", "learn:badges", "learn:certificate"]:
        response = client.get(reverse(name))
        assert response.status_code == 302
        assert "/login/" in response.url


# --------------------------------------------------------------------------
# Dashboard — momentum redesign
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_zero_progress_student_gets_the_full_dashboard(client_student, modules):
    """A brand-new, zero-progress Bronze student must get the SAME full dashboard
    as everyone else (profile card, tier panel, stats, calendar) — not a stripped
    'welcome' fork. This is the regression guard for that bug."""
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-chip__btn" in html                # the top-right profile chip
    assert "cy-tierpanel" in html                # the tier panel, with its emblem
    assert "cy-tier--bronze" in html             # Bronze for a 0-point student
    assert "to Silver" in html                   # progress toward the next tier
    assert html.count("cy-stat__v") == 6         # six stat cards in a 3 x 2 grid
    assert "cy-cal__grid" in html                # the activity calendar
    assert "cy-welcome" not in html              # NOT the old welcome fork
    assert html.count("cy-btn--primary") == 1    # one clear "Start" action


@pytest.mark.django_db
def test_a_returning_student_sees_the_continue_action_and_rank(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-dhero" in html                    # the Continue hero card
    assert "Cyber Aware" in html                 # the rank title, in the profile
    assert html.count("cy-btn--primary") == 1    # the single Continue


@pytest.mark.django_db
def test_module_checklist_lives_on_the_progress_page_not_the_dashboard(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    dash = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-course__list" not in dash         # the checklist is relocated off page 1
    prog = client_student.get(reverse("learn:progress")).content.decode()
    assert "Module by module" in prog            # it lives on My progress
    assert modules[0].title in prog


@pytest.mark.django_db
def test_the_streak_nudges_when_a_day_is_at_risk(client_student, student, modules):
    import datetime

    from django.utils import timezone

    # Active yesterday, not yet today → at risk.
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    profile = student.profile
    profile.streak_count = 4
    profile.last_active = timezone.make_aware(
        datetime.datetime.combine(
            timezone.localdate() - datetime.timedelta(days=1), datetime.time(12, 0)
        )
    )
    profile.save(update_fields=["streak_count", "last_active"])

    html = client_student.get(reverse("dashboard")).content.decode()
    # Streak is a stat card; its at-risk state and nudge survive.
    assert "cy-stat--at_risk" in html
    assert "Streak at risk" in html            # the concise at-risk nudge, in the card
    assert 'cy-stat__v">4<' in html            # the 4-day streak count is shown


@pytest.mark.django_db
def test_dashboard_stats_strip_shows_real_totals(client_student, student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    # Six stat cards in one 3 x 2 grid.
    assert "cy-db__stats" in html
    assert html.count("cy-stat__v") == 6
    assert html.count("cy-stat ") + html.count('cy-stat"') >= 6


# --------------------------------------------------------------------------
# Dashboard — professional layout (stat tiles, rail, quest marker)
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_returning_dashboard_has_the_profile_and_stats(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-chip__btn" in html            # the clickable profile chip (a disclosure)
    assert "cy-chip__name" in html           # the student's name
    assert "cy-chip__tier" in html           # tier shown on the chip
    assert html.count("cy-stat__v") == 6


def _set_points(student, points):
    from modules import gamification as g

    profile = g.get_profile(student)
    profile.points = points
    profile.save(update_fields=["points"])


@pytest.mark.django_db
def test_dashboard_shows_the_tier_and_progress_to_next(client_student, student, modules):
    """The tier emblem, its name and 'points to next' are real, from points."""
    _set_points(student, 700)             # Gold (500); Platinum at 1000
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-tier--gold" in html        # the tier panel carries the metal
    assert "cy-tierpanel" in html         # the tier panel with its progress
    assert "200 / 500" in html            # into-band / band-span (700-500 / 1000-500)
    assert "to Platinum" in html


@pytest.mark.django_db
def test_dashboard_top_tier_hides_the_progress_line(client_student, student, modules):
    _set_points(student, 2000)            # Diamond, the top tier
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-tier--diamond" in html          # the tier is still shown, cleanly
    assert "Top tier reached" in html          # a calm mastery state
    assert "cy-tierpanel__prog" not in html    # no 'to next' bar at the top tier


@pytest.mark.django_db
def test_dashboard_calendar_has_a_heat_legend_and_marks_activity(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-cal__legend" in html
    assert "cy-cal__heatkey" in html      # the Less→More heat scale
    assert "Less" in html and "More" in html
    assert "is-active is-l" in html       # a real active day carries a heat level
    assert "active day" in html           # the "X active days this month" summary
    assert "data-tip=" in html            # a hover/tap tooltip on the active day
    assert "1 lesson" in html             # typed: what was done that day


@pytest.mark.django_db
def test_the_tier_is_shown_distinctly_per_rank(client_student, student, modules):
    """Each tier carries its own metal via the tier class, so Gold and Diamond
    read as visibly different ranks (pill + avatar), not the same chip recoloured."""
    _set_points(student, 700)             # Gold
    gold = client_student.get(reverse("dashboard")).content.decode()
    _set_points(student, 2000)            # Diamond
    diamond = client_student.get(reverse("dashboard")).content.decode()

    assert "cy-tier--gold" in gold
    assert "cy-tier--diamond" in diamond
    assert "cy-tier--gold" not in diamond   # the rank genuinely changes


@pytest.mark.django_db
def test_dashboard_celebrates_a_new_tier_once(client_student, student, modules):
    from modules import gamification as g

    profile = g.get_profile(student)
    profile.points = 700                   # Gold (index 2)
    profile.celebrated_tier = 1            # last congratulated at Silver
    profile.save(update_fields=["points", "celebrated_tier"])

    first = client_student.get(reverse("dashboard")).content.decode()
    assert "You reached Gold" in first
    assert "cy-celebrate" in first

    profile.refresh_from_db()
    assert profile.celebrated_tier == 2    # marker advanced

    second = client_student.get(reverse("dashboard")).content.decode()
    assert "You reached Gold" not in second   # never repeats


@pytest.mark.django_db
def test_the_composed_dashboard_sections_are_present(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-db__hero" in html             # Continue hero + tier panel
    assert "cy-tierpanel" in html            # the tier panel with emblem
    assert "cy-db__stats" in html            # the six-card stat grid
    assert "cy-db__lower" in html            # main (up next + goal) + rail (calendar + nudge)
    assert "cy-cal__grid" in html            # the calendar
    assert "cy-upnext" in html               # the new "Up next" roadmap
    assert "cy-goal" in html                 # the new weekly goal


@pytest.mark.django_db
def test_up_next_shows_the_current_module_and_locks_the_one_after(client_student, modules):
    """The Up next roadmap surfaces the module you're on (current) and the next
    one, still locked. DEBUG is False under test, so the real lock is exercised."""
    for n in (1, 2, 3, 4):
        complete(client_student, modules[0], n, HTTP_X_REQUESTED_WITH="fetch")
    complete(client_student, modules[1], 1, HTTP_X_REQUESTED_WITH="fetch")

    html = client_student.get(reverse("dashboard")).content.decode()
    assert "cy-mrow--current" in html        # the module in progress
    assert "cy-mrow--locked" in html         # the next one, still locked
    assert modules[1].title in html


@pytest.mark.django_db
def test_weekly_goal_reflects_real_activity(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()
    assert "Weekly goal" in html
    assert "cy-goal__ring" in html
    assert html.count("cy-goal__days") == 1   # one day-marker strip
    assert html.count("cy-goal__day ") + html.count('cy-goal__day"') == 7   # Mon..Sun
    # The lesson completed just now makes today an active study day: at least 1/5.
    assert "1/5" in html


@pytest.mark.django_db
def test_student_nav_context_processor_powers_the_shared_chip(student, author, rf):
    """The chip's data comes from a context processor, so it is reusable on any
    student page (dashboard, module overview) without per-view wiring. Students
    get a profile; administrators and anonymous users get nothing."""
    from django.contrib.auth.models import AnonymousUser

    from nstp.context_processors import student_nav

    req = rf.get("/")
    req.user = student
    ctx = student_nav(req)
    assert ctx["nav_profile"]["name"]
    assert ctx["nav_profile"]["tier"].tier.name
    assert ctx["nav_profile"]["level"].level >= 1

    req.user = author  # an ADMINISTRATOR — uses console chrome, not the chip
    assert student_nav(req) == {}

    req.user = AnonymousUser()
    assert student_nav(req) == {}


@pytest.mark.django_db
def test_module_overview_carries_the_shared_profile_chip(client_student, modules):
    """The module overview uses the same chip as the dashboard, top right."""
    html = client_student.get(reverse("learn:module", args=[modules[0].order_index])).content.decode()
    assert "cy-topbar--page" in html
    assert "cy-chip__btn" in html


# --------------------------------------------------------------------------
# Study calendar — a real month view in the dashboard rail
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_dashboard_shows_the_activity_calendar_with_todays_study(client_student, modules):
    from django.utils import timezone

    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()

    assert "cy-cal" in html
    assert timezone.localdate().strftime("%B %Y") in html   # e.g. "July 2026"
    assert "<strong>1</strong> active day this month" in html
    # Today's completion is marked active (with a heat level) and as today.
    assert "cy-cal__day is-active is-l1 is-today" in html


@pytest.mark.django_db
def test_calendar_does_not_page_into_the_future(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("dashboard")).content.decode()
    # On the current month the forward arrow is disabled, not a link.
    assert "cy-cal__nav is-disabled" in html
    assert "cal_month=" in html   # the back arrow still carries navigation params


@pytest.mark.django_db
def test_calendar_arrows_navigate_to_another_month(client_student, modules):
    import datetime

    from django.utils import timezone

    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    # Page back one month using the same params the arrows carry.
    last_month = timezone.localdate().replace(day=1) - datetime.timedelta(days=1)
    html = client_student.get(
        reverse("dashboard"), {"cal_year": last_month.year, "cal_month": last_month.month}
    ).content.decode()

    assert last_month.strftime("%B %Y") in html
    # From a past month you can page forward again — the arrow is live.
    assert "cy-cal__nav is-disabled" not in html


@pytest.mark.django_db
def test_calendar_falls_back_to_this_month_on_bad_params(client_student, modules):
    from django.utils import timezone

    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    this_month = timezone.localdate().strftime("%B %Y")

    for bad in ({"cal_month": "13"}, {"cal_month": "oops"}, {"cal_year": "x"}):
        html = client_student.get(reverse("dashboard"), bad).content.decode()
        assert this_month in html


# --------------------------------------------------------------------------
# Badges gallery — tiers, collectibles, teased locked
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_badges_gallery_is_grouped_into_tiers_with_counts(client_student, modules):
    html = client_student.get(reverse("learn:badges")).content.decode()
    for tier in ["Getting Started", "Knowledge", "Milestones", "Streaks"]:
        assert tier in html
    assert "of 11 earned" in html          # overall completion header


@pytest.mark.django_db
def test_locked_badges_still_tease_how_to_earn_them(client_student, modules):
    html = client_student.get(reverse("learn:badges")).content.decode()
    # The quiz badge is locked (no quizzes yet) but shows its how-to.
    assert "Pass your first quiz" in html
    assert "cy-collect__lock" in html      # the lock chip
    assert "cy-collect is-locked" in html


@pytest.mark.django_db
def test_earned_badges_show_as_earned(client_student, modules):
    complete(client_student, modules[0], 1, HTTP_X_REQUESTED_WITH="fetch")
    html = client_student.get(reverse("learn:badges")).content.decode()
    assert "cy-collect is-earned" in html


def test_every_badge_has_a_distinct_icon_in_the_sprite():
    import pathlib

    from modules.badges import CATALOGUE

    sprite = pathlib.Path("templates/_icons.html").read_text()
    icons = [b.icon for b in CATALOGUE]
    for icon in icons:
        assert f'id="{icon}"' in sprite, f"{icon} missing from the icon sprite"
    # streaks aside, the set is distinct — not one shape repeated
    assert len(set(icons)) >= len(icons) - 1


# --------------------------------------------------------------------------
# Certificate — the document design and its honest states
# --------------------------------------------------------------------------


def complete_all_modules(client, modules):
    """Complete every lesson of every module (respecting the sequential lock)."""
    for module in modules:
        for lesson in module.lessons.order_by("lesson_number"):
            complete(client, module, lesson.lesson_number, HTTP_X_REQUESTED_WITH="fetch")


@pytest.mark.django_db
def test_certificate_is_a_locked_preview_before_completion(
    client_student, student, modules
):
    html = client_student.get(reverse("learn:certificate")).content.decode()
    # The formal diploma is shown, but locked and clearly not yet earned.
    assert "cy-dip" in html
    assert "cy-dip cy-dip--locked" in html   # the locked modifier is applied
    assert "not yet earned" in html.lower()
    assert f"of {len(modules)} modules" in html   # the progress note
    assert student.email in html                  # real data: the recipient


@pytest.mark.django_db
def test_certificate_hides_the_code_and_download_until_earned(
    client_student, modules
):
    html = client_student.get(reverse("learn:certificate")).content.decode()
    # A masked placeholder, never a real or "verified" code, and no PDF yet.
    assert "CYB-" in html
    assert "issued on completion" in html
    assert reverse("certificates:download") not in html


@pytest.mark.django_db
def test_the_issued_serial_is_stable_for_a_given_student(client_student, modules):
    import re

    complete_all_modules(client_student, modules)
    first = client_student.get(reverse("learn:certificate")).content.decode()
    second = client_student.get(reverse("learn:certificate")).content.decode()
    code = re.search(r"CYB-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}", first)
    assert code is not None
    assert code.group(0) in second               # one certificate, stable serial


@pytest.mark.django_db
def test_earning_the_certificate_drops_the_preview_and_issues_it(
    client_student, student, modules
):
    from django.utils import timezone

    from certificates.models import Certificate

    complete_all_modules(client_student, modules)

    html = client_student.get(reverse("learn:certificate")).content.decode()
    assert "cy-dip" in html
    assert "cy-dip cy-dip--locked" not in html        # no longer a locked preview
    assert "not yet earned" not in html.lower()
    assert str(timezone.localdate().year) in html     # a real issue date
    assert reverse("certificates:download") in html   # the downloadable PDF
    # A real certificate row was issued, and its serial is on the page.
    cert = Certificate.objects.get(user=student)
    assert cert.serial in html


# --------------------------------------------------------------------------
# Interactive lesson room — tasks, per-task completion, XP, no-JS fallback
# --------------------------------------------------------------------------

from modules.models import LessonTask, TaskProgress


def add_tasks(lesson, specs):
    """specs: list of (kind, points). Check/scenario tasks get a 2-option payload."""
    out = []
    for i, (kind, points) in enumerate(specs, start=1):
        payload = {}
        if kind != "CONCEPT":
            payload = {
                "question": "Which is safe?",
                "options": [
                    {"text": "The safe one", "correct": True, "explanation": "Yes — this is right."},
                    {"text": "The risky one", "correct": False, "explanation": "No — this is a trap."},
                ],
            }
        out.append(
            LessonTask.objects.create(
                lesson=lesson, order=i, task_key=f"k{i}", kind=kind,
                points=points, body="<p>Teaching.</p>", payload=payload,
            )
        )
    return out


def post_task(client, module, lesson, task):
    return client.post(
        reverse("learn:complete_task", args=[module.order_index, lesson.lesson_number]),
        {"task": task.id},
    )


@pytest.mark.django_db
def test_a_task_lesson_renders_the_interactive_room(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_tasks(lesson, [("CONCEPT", 3), ("CHECK", 3), ("SCENARIO", 4)])

    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert "data-room" in html
    assert html.count("data-task-id=") == 3     # one section per task
    assert "lesson.js" in html
    assert "The safe one" in html and "this is a trap" in html.lower()


@pytest.mark.django_db
def test_completing_every_task_banks_the_lesson_and_returns_the_reward(client_student, modules, student):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    tasks = add_tasks(lesson, [("CONCEPT", 2), ("CHECK", 3), ("SCENARIO", 5)])

    r1 = post_task(client_student, modules[0], lesson, tasks[0]).json()
    assert r1["lesson_completed"] is False
    assert r1["lesson_points_done"] == 2

    post_task(client_student, modules[0], lesson, tasks[1])
    r3 = post_task(client_student, modules[0], lesson, tasks[2]).json()
    assert r3["lesson_completed"] is True
    assert r3["reward"]["points_gained"] == 50
    assert ProgressRecord.objects.filter(user=student, lesson=lesson).exists()


@pytest.mark.django_db
def test_a_completed_task_shows_as_done_on_return(client_student, modules, student):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    tasks = add_tasks(lesson, [("CONCEPT", 5), ("CONCEPT", 5)])
    post_task(client_student, modules[0], lesson, tasks[0])

    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    # the first task carries the done marker, the second doesn't
    assert f'data-task-id="{tasks[0].id}"' in html
    idx = html.index(f'data-task-id="{tasks[0].id}"')
    assert 'data-done="1"' in html[idx - 120:idx + 200]


@pytest.mark.django_db
def test_a_task_lesson_still_completes_without_js(client_student, modules, student):
    """The no-JS fallback: the plain mark-complete endpoint still banks the lesson."""
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_tasks(lesson, [("CONCEPT", 5), ("CHECK", 5)])

    complete(client_student, modules[0], lesson.lesson_number, HTTP_X_REQUESTED_WITH="fetch")
    assert ProgressRecord.objects.filter(user=student, lesson=lesson).exists()


@pytest.mark.django_db
def test_task_completion_respects_the_module_lock(client_student, modules):
    locked_lesson = modules[1].lessons.order_by("lesson_number").first()
    tasks = add_tasks(locked_lesson, [("CONCEPT", 10)])
    resp = post_task(client_student, modules[1], locked_lesson, tasks[0])
    assert resp.status_code == 403


@pytest.mark.django_db
def test_task_lesson_page_is_clean_and_without_emoji(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    # Include an activity task so the activity branch of the template is exercised
    # (a past leak lived only in that branch).
    add_tasks(lesson, [("CONCEPT", 4), ("SCENARIO", 3)])
    add_activity(lesson, 3, "hz-sort", "SORT", 3, {
        "prompt": "Sort them.", "buckets": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}],
        "items": [{"id": "1", "text": "x", "bucket": "a", "why": "y"}],
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    for token in LEAKS:
        assert token not in html
    assert not EMOJI.findall(html)


# --------------------------------------------------------------------------
# Diagrams — inline CSS/SVG partials, CSP-safe, clean
# --------------------------------------------------------------------------

from django.template.loader import render_to_string


def test_each_diagram_renders_its_content():
    cases = {
        "net-topology": "Attached devices",
        "data-hops": "Spring2024!",
        "data-journey": "Connection is secure",
        "cia-triad": "Confidentiality",
        "network-path": "Your router",
        "router-admin": "Admin password",
        "scam-email": "auspost-au-secure.info",
        "email-invoice": "bunya-supplies-billing.com",
        "security-settings": "Two-factor authentication",
        "device-checklist": "Disk encryption",
        "fake-update": "free-hd-movies-stream.info",
        "enable-macros": "Enable Content",
        "scareware-popup": "1800 631 442",
        "router-wifi": "YarraRidge-Office",
        "lookalike-login": "yarravi11ere",
        "phish-headers": "m365-account-verify.co",
        "smishing-linkt": "linkt-au-pay.info",
        "compose-send": "Passport_Nguyen.pdf",
        "fw-default": "Default action",
        "ir-alert": "RECEPTION-PC",
        "ransom-screen": "files have been encrypted",
        "download-trap": "report_2026.pdf",
        "attachment-exe": "Invoice_4471.pdf.exe",
        "locked-files": "photos.jpg.locked",
        "breach-email": "Rivertown Books",
        "sms-phish": "aus-post-redelivery.info",
        "exec-email": "ceo-office-mail.com",
        "caller-id": "Sarah Whitton",
        "msg-encrypted": "Encrypted",
        "secure-share": "Restricted to specific people",
        "wifi-evil-twin": "Corner Cafe Free WiFi",
        "net-scene": "YOUR NETWORK",
        "scene-vish": "keep it",
        "scene-send": "Client_medical_form.pdf",
        "wifi-devices": "UNKNOWN DEVICE",
        "firewall-flow": "Wanted traffic passes",
        "segment-flow": "seals it into one zone",
        "incident-escalation": "scare and a disaster",
        "recovery-board": "one system at a time",
        "secure-bars": "cybaroo-clinic.com.au",
        "data-travels": "Your device",
        "phishing-email": "flour-supplier-au.info",
        "two-factor": "code on your phone",
        "defence-in-depth": "What matters",
    }
    for key, needle in cases.items():
        html = render_to_string("modules/_diagram.html", {"key": key})
        assert "cy-diagram" in html
        assert needle in html
        # inline only — no external image or script
        assert "<img" not in html and "<script" not in html
        for token in LEAKS:
            assert token not in html
        assert not EMOJI.findall(html)


def test_an_unknown_diagram_key_renders_nothing():
    assert render_to_string("modules/_diagram.html", {"key": "does-not-exist"}).strip() == ""


# --------------------------------------------------------------------------
# Interactive activities — container + CSP-safe JSON config + script wiring
# --------------------------------------------------------------------------

import json as _json


def add_activity(lesson, order, task_key, kind, points, payload):
    return LessonTask.objects.create(
        lesson=lesson, order=order, task_key=task_key, kind=kind,
        points=points, body="", payload=payload,
    )


@pytest.mark.django_db
def test_sort_activity_renders_container_and_json_config(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-sort", "SORT", 10, {
        "prompt": "Sort them.",
        "buckets": [{"id": "safe", "label": "Safe"}, {"id": "risky", "label": "Risky"}],
        "items": [{"id": "a", "text": "WPA3", "bucket": "safe", "why": "modern"}],
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()

    assert 'data-activity data-activity-kind="SORT"' in html
    assert 'data-config="t-sort"' in html
    # CSP-safe config: inert application/json, not an executable script
    assert '<script id="t-sort" type="application/json">' in html
    assert "activities.js" in html
    # the config actually carries the payload
    frag = html.split('<script id="t-sort" type="application/json">', 1)[1].split("</script>", 1)[0]
    cfg = _json.loads(frag)
    assert {b["id"] for b in cfg["buckets"]} == {"safe", "risky"}


@pytest.mark.django_db
def test_spot_activity_config_marks_the_fake(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-spot", "SPOT", 10, {
        "prompt": "Pick the scam.",
        "left": {"sender": "AusPost", "text": "real one"},
        "right": {"sender": "AusPost", "text": "scam one"},
        "fake": "right", "why": "lookalike link",
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert 'data-activity-kind="SPOT"' in html
    frag = html.split('<script id="t-spot" type="application/json">', 1)[1].split("</script>", 1)[0]
    assert _json.loads(frag)["fake"] == "right"


@pytest.mark.django_db
def test_activity_completion_banks_through_the_normal_path(client_student, modules, student):
    """Whatever the UI, completing the activity task records + banks like any task."""
    lesson = modules[0].lessons.order_by("lesson_number").first()
    task = add_activity(lesson, 1, "t-sort", "SORT", 10, {
        "prompt": "x", "buckets": [{"id": "a", "label": "A"}],
        "items": [{"id": "1", "text": "x", "bucket": "a", "why": "y"}],
    })
    resp = post_task(client_student, modules[0], lesson, task)
    assert resp.status_code == 200
    assert resp.json()["lesson_completed"] is True   # single task lesson
    assert ProgressRecord.objects.filter(user=student, lesson=lesson).exists()


@pytest.mark.django_db
def test_inbox_activity_renders_with_findable_tells(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-inbox", "INBOX", 10, {
        "prompt": "Find the tells.",
        "parts": [
            {"id": "from", "zone": "From", "text": "svc@auspost-delivery.info", "bad": True, "why": "lookalike"},
            {"id": "b1", "zone": "Body", "text": "context sentence", "bad": False, "why": "fine"},
        ],
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert 'data-activity-kind="INBOX"' in html and "activities.js" in html
    frag = html.split('<script id="t-inbox" type="application/json">', 1)[1].split("</script>", 1)[0]
    cfg = _json.loads(frag)
    assert sum(1 for p in cfg["parts"] if p["bad"]) == 1


@pytest.mark.django_db
def test_password_activity_renders_with_its_rules(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-pw", "PASSWORD", 10, {
        "prompt": "Build one.", "target": "strong",
        "common": ["password", "123456"], "tips": ["longer is better"],
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert 'data-activity-kind="PASSWORD"' in html
    frag = html.split('<script id="t-pw" type="application/json">', 1)[1].split("</script>", 1)[0]
    cfg = _json.loads(frag)
    assert cfg["target"] == "strong" and "password" in cfg["common"]


@pytest.mark.django_db
def test_branch_activity_renders_a_scenario_that_reaches_an_ending(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-branch", "BRANCH", 10, {
        "prompt": "Decide.",
        "start": "n1",
        "nodes": {
            "n1": {"text": "An urgent invoice arrives.", "choices": [
                {"label": "Verify by phone", "to": "end", "outcome": "good", "feedback": "Right."},
                {"label": "Pay now", "to": "n1bad", "outcome": "bad", "feedback": "Scam."},
            ]},
            "n1bad": {"text": "The money's gone.", "choices": [{"label": "See the better path", "to": "end"}]},
            "end": {"text": "Verify before you pay.", "choices": []},
        },
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert 'data-activity-kind="BRANCH"' in html
    frag = html.split('<script id="t-branch" type="application/json">', 1)[1].split("</script>", 1)[0]
    cfg = _json.loads(frag)
    assert cfg["start"] in cfg["nodes"]
    assert any(not n["choices"] for n in cfg["nodes"].values())   # has an ending


# --------------------------------------------------------------------------
# Framework upgrades: check hints + spot-the-fake login variant
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_check_with_a_hint_renders_a_hint_toggle_and_hint(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    LessonTask.objects.create(
        lesson=lesson, order=1, task_key="c1", kind="CHECK", points=10,
        payload={
            "question": "Which is safe?",
            "hint": "Think about who controls the network.",
            "options": [
                {"text": "Right one", "correct": True, "explanation": "Yes."},
                {"text": "Wrong one", "correct": False, "explanation": "No."},
            ],
        },
    )
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert "data-hint-toggle" in html
    assert "Need a hint?" in html
    assert "Think about who controls the network." in html


@pytest.mark.django_db
def test_a_check_without_a_hint_shows_no_hint_control(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    LessonTask.objects.create(
        lesson=lesson, order=1, task_key="c2", kind="CHECK", points=10,
        payload={"question": "Q?", "hint": "", "options": [
            {"text": "a", "correct": True, "explanation": "y"},
            {"text": "b", "correct": False, "explanation": "n"},
        ]},
    )
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    assert "data-hint-toggle" not in html


@pytest.mark.django_db
def test_spot_login_variant_config_carries_urls_and_the_fake(client_student, modules):
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_activity(lesson, 1, "t-login", "SPOT", 10, {
        "prompt": "Which login is fake?",
        "variant": "login",
        "left": {"url": "https://coastline.com.au/login", "brand": "Coastline"},
        "right": {"url": "https://coastline-secure-login.com/", "brand": "Coastline"},
        "fake": "right", "why": "The domain isn't coastline.com.au.",
    })
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    frag = html.split('<script id="t-login" type="application/json">', 1)[1].split("</script>", 1)[0]
    cfg = _json.loads(frag)
    assert cfg["variant"] == "login"
    assert cfg["fake"] == "right"
    assert "coastline-secure-login.com" in cfg["right"]["url"]


# --------------------------------------------------------------------------
# Lesson rail navigation — anchors point to the right tasks; active states
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_lesson_rail_links_point_to_their_own_tasks_in_order(client_student, modules):
    """Every rail task link (jump + anchor) points to its OWN panel, in order, so
    clicking a task can never jump to an unrelated / past question."""
    lesson = modules[0].lessons.order_by("lesson_number").first()
    tasks = add_tasks(lesson, [("CONCEPT", 3), ("CONCEPT", 3), ("CONCEPT", 4)])
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    ids = [str(t.id) for t in tasks]
    jumps = re.findall(r'data-task-jump="(\d+)"', html)
    anchors = re.findall(r'href="#task-(\d+)"', html)
    panels = re.findall(r'data-task-id="(\d+)"', html)
    items = re.findall(r'data-tasklist-item data-for="(\d+)"', html)
    assert jumps == anchors == panels == items == ids


@pytest.mark.django_db
def test_lesson_rail_marks_done_and_current_tasks(client_student, student, modules):
    """The rail reflects real progress: a completed task is ticked (is-done) and
    the next unfinished task is highlighted (is-current)."""
    from modules.models import TaskProgress

    lesson = modules[0].lessons.order_by("lesson_number").first()
    tasks = add_tasks(lesson, [("CONCEPT", 3), ("CONCEPT", 3), ("CONCEPT", 4)])
    TaskProgress.objects.create(user=student, task=tasks[0])
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()

    def cls_for(tid):
        m = re.search(r'cy-tasklist__item ([^"]*)"[^>]*?data-for="%s"' % tid, html, re.S)
        return m.group(1) if m else "MISSING"

    assert "is-done" in cls_for(tasks[0].id)
    assert "is-current" in cls_for(tasks[1].id)


@pytest.mark.django_db
def test_lesson_rail_links_to_every_lesson_and_marks_current(client_student, modules):
    """The rail's Lessons stepper links to every lesson in the module (so clicking
    a lesson opens that lesson), and marks the current one."""
    lesson = modules[0].lessons.order_by("lesson_number").first()
    add_tasks(lesson, [("CONCEPT", 5), ("CONCEPT", 5)])
    html = client_student.get(
        reverse("learn:lesson", args=[modules[0].order_index, lesson.lesson_number])
    ).content.decode()
    for s in modules[0].lessons.all():
        assert reverse("learn:lesson", args=[modules[0].order_index, s.lesson_number]) in html
    assert "cy-stepper__dot is-current" in html
