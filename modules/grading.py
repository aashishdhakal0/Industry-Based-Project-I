"""Performance tiers — Distinction / Merit / Pass / Not yet.

A client request (CLAUDE.md §6). Pure and derived entirely from QuizResult:
there is no grade field and no new model. A module's grade is the tier of the
student's BEST score on that module's quiz; an overall grade is the tier of the
mean of those best scores. Because it reads the same rows the gamification
engine trusts, a grade can never disagree with "did they pass".

Kept here in `modules` (near the data) rather than in the staff app so the
certificate can reuse it later.
"""

from dataclasses import dataclass

from django.db.models import Max

from quizzes.models import QuizResult


@dataclass(frozen=True)
class Tier:
    slug: str
    name: str
    min_score: int  # inclusive lower bound of the band


# Ordered high to low. The bands the client specified: Distinction 90-100,
# Merit 80-89, Pass 70-79, Not yet 0-69.
DISTINCTION = Tier("distinction", "Distinction", 90)
MERIT = Tier("merit", "Merit", 80)
PASS = Tier("pass", "Pass", 70)
NOT_YET = Tier("not-yet", "Not yet", 0)

# A learner who has never attempted a quiz has no grade at all — distinct from
# scoring low. It carries min_score -1 so it never matches a real score.
NOT_STARTED = Tier("not-started", "Not started", -1)

# The four real bands, for building a distribution or a legend. NOT_STARTED is
# deliberately excluded — it is the absence of a grade, not a band.
BANDS = (DISTINCTION, MERIT, PASS, NOT_YET)


def tier_for_score(score):
    """The tier a percentage falls in. None (no attempt) → NOT_STARTED."""
    if score is None:
        return NOT_STARTED
    for tier in BANDS:
        if score >= tier.min_score:
            return tier
    return NOT_YET  # unreachable (NOT_YET.min_score == 0), kept for clarity


def best_scores_by_module(user):
    """{module_id: best score} across every attempt the user has made.

    One query. The best attempt drives the grade, so a student who nails a
    retake is graded on that, not on an early fail.
    """
    rows = (
        QuizResult.objects.filter(user=user)
        .values("quiz__module_id")
        .annotate(best=Max("score"))
    )
    return {row["quiz__module_id"]: row["best"] for row in rows}


def module_tier(user, module):
    """The grade tier for one module, from the user's best attempt on it."""
    return tier_for_score(best_scores_by_module(user).get(module.id))


def overall_grade(user):
    """The course grade: (mean best score, tier).

    Averaged over the module quizzes the student has actually attempted, so an
    untouched module doesn't drag a strong average down to a fail. Returns
    (None, NOT_STARTED) when nothing has been attempted.
    """
    best = best_scores_by_module(user)
    return grade_from_scores(best.values())


def grade_from_scores(scores):
    """(mean rounded to a whole percent, tier) for an iterable of best scores.

    The shared core so the single-user path and the admin's bulk path grade
    identically. Empty → (None, NOT_STARTED).
    """
    scores = [s for s in scores if s is not None]
    if not scores:
        return None, NOT_STARTED
    mean = round(sum(scores) / len(scores))
    return mean, tier_for_score(mean)
