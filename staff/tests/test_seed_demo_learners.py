"""The demo-learner seed: realistic spread, honest numbers, idempotent."""

import pytest
from django.core.management import call_command

from authentication.models import User
from modules.grading import overall_grade
from modules.models import Lesson, Module
from quizzes.models import Quiz, QuizResult
from staff.management.commands.seed_demo_learners import DEMO_EMAILS, LEARNERS


@pytest.fixture
def content(db):
    """Six published modules, each with four lessons and an active quiz."""
    admin = User.objects.create_user(
        email="seed-admin@example.com", password="x", role=User.Role.ADMINISTRATOR
    )
    for i in range(1, 7):
        m = Module.objects.create(
            title=f"Module {i}", order_index=i, is_published=True, created_by=admin
        )
        for n in range(1, 5):
            Lesson.objects.create(module=m, lesson_number=n, title=f"L{n}")
        Quiz.objects.create(module=m, is_active=True, pass_mark=70)


@pytest.fixture
def seeded(content):
    call_command("seed_demo_learners")


def _by_email(email):
    return User.objects.get(email=email)


def test_creates_all_learners_as_active_verified_students(seeded):
    learners = User.objects.filter(email__in=DEMO_EMAILS)
    assert learners.count() == len(LEARNERS)
    for u in learners:
        assert u.role == User.Role.STUDENT
        assert u.is_active and u.is_verified
        assert u.profile is not None


def test_points_match_progress_records_are_truth(seeded):
    # Priya finished all six: 24 lessons * 40 + 6 quizzes * 200 = 2160.
    priya = _by_email("priya.nadesan@gmail.com")
    assert priya.profile.points == 2160
    # Ethan has only started (2 lessons, no quiz): 80 points.
    ethan = _by_email("ethan.wilson@gmail.com")
    assert ethan.profile.points == 80


def test_grades_match_the_quiz_scores(seeded):
    priya = _by_email("priya.nadesan@gmail.com")
    assert overall_grade(priya)[1].slug == "distinction"
    daniel = _by_email("d.papadopoulos@riversideshire.gov.au")
    assert overall_grade(daniel)[1].slug == "merit"
    jack = _by_email("jackt87@gmail.com")
    assert overall_grade(jack)[1].slug == "pass"
    ethan = _by_email("ethan.wilson@gmail.com")
    assert overall_grade(ethan)[1].slug == "not-started"


def test_scores_are_not_all_round_numbers(seeded):
    scores = list(
        QuizResult.objects.filter(passed=True).values_list("score", flat=True)
    )
    assert scores
    # A believable mix: at least some scores aren't multiples of five.
    assert any(s % 5 != 0 for s in scores)


def test_a_retake_produces_two_attempts(seeded):
    # Grace failed module 3 once before passing it (retakes=[3]).
    grace = _by_email("grace.nguyen@yarraridgeps.vic.edu.au")
    attempts = QuizResult.objects.filter(user=grace, quiz__module__order_index=3)
    assert attempts.count() == 2
    assert attempts.filter(passed=False).exists()
    assert attempts.filter(passed=True).exists()


def test_needs_attention_is_populated(seeded):
    from staff import services

    attention = services.overview(services.collect_learners())["attention"]
    emails = {r.user.email for r in attention}
    assert "mohammed.ali@bigpond.com" in emails      # flagged + inactive
    assert "noah.smith@coastlineplumbing.com.au" in emails  # 25 days quiet
    # At least one is flagged and at least one is inactive.
    assert any(r.flagged for r in attention)
    assert any(r.inactive for r in attention)


def test_activity_dates_are_spread_not_all_now(seeded):
    from django.utils import timezone

    last_actives = [
        u.profile.last_active for u in User.objects.filter(email__in=DEMO_EMAILS)
    ]
    now = timezone.now()
    days = sorted({(now - la).days for la in last_actives})
    # Recent AND long-lapsed learners both exist.
    assert min(days) <= 1
    assert max(days) >= 14


def test_idempotent_rerun_does_not_duplicate(seeded):
    before_users = User.objects.filter(email__in=DEMO_EMAILS).count()
    before_results = QuizResult.objects.count()

    call_command("seed_demo_learners")

    assert User.objects.filter(email__in=DEMO_EMAILS).count() == before_users
    assert QuizResult.objects.count() == before_results


def test_clear_removes_the_demo_learners(seeded):
    call_command("seed_demo_learners", "--clear")
    assert not User.objects.filter(email__in=DEMO_EMAILS).exists()
