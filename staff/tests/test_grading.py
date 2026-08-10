"""Grade tiers — the band maths, in isolation."""

import pytest

from modules.grading import (
    DISTINCTION,
    MERIT,
    NOT_STARTED,
    NOT_YET,
    PASS,
    grade_from_scores,
    tier_for_score,
)


@pytest.mark.parametrize(
    "score,tier",
    [
        (100, DISTINCTION),
        (90, DISTINCTION),   # lower edge of Distinction
        (89, MERIT),         # just below
        (80, MERIT),
        (79, PASS),
        (70, PASS),          # the pass mark
        (69, NOT_YET),
        (0, NOT_YET),
        (None, NOT_STARTED), # never attempted
    ],
)
def test_tier_for_score_bands(score, tier):
    assert tier_for_score(score) is tier


def test_grade_from_scores_is_the_mean_then_the_tier():
    # (90 + 80 + 70) / 3 = 80 -> Merit
    score, tier = grade_from_scores([90, 80, 70])
    assert score == 80
    assert tier is MERIT


def test_grade_from_scores_ignores_missing_and_empty():
    assert grade_from_scores([]) == (None, NOT_STARTED)
    assert grade_from_scores([None, None]) == (None, NOT_STARTED)
    # None values are dropped, not counted as zero.
    score, _ = grade_from_scores([100, None])
    assert score == 100
