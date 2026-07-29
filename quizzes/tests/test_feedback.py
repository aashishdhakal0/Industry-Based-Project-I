"""The Adaptive Feedback Engine — grouping, ranking, explanations, no N+1.

The differentiator's core: every mistake is explained from the option's own
explanation_text and traced to the lesson that teaches it, and the lessons are
ranked by where the mistakes clustered.
"""

import pytest

from quizzes import feedback as afe
from quizzes import services as svc

from .conftest import responses_for


def _attempt(student, quiz, *, correct):
    """Sit the whole bank (so lesson spread is deterministic) and record it."""
    questions = list(quiz.questions.order_by("ordering").prefetch_related("answers"))
    ids = [q.id for q in questions]
    result, _, _ = svc.grade_and_record(
        student, quiz, ids, responses_for(questions, correct=correct)
    )
    return result


@pytest.mark.django_db
def test_a_perfect_attempt_yields_an_empty_plan(student, quiz):
    result = _attempt(student, quiz, correct=12)
    fb = afe.analyse(result)
    assert fb.wrong_count == 0 and fb.plan == []


@pytest.mark.django_db
def test_each_wrong_question_is_explained_from_both_options(student, quiz):
    # Answer only the first question correctly; the rest are wrong.
    result = _attempt(student, quiz, correct=1)
    fb = afe.analyse(result)

    assert fb.wrong_count == 11
    item = fb.items[0]
    # The chosen (wrong) option and the correct one both carry their explanation.
    assert item.your_why == "Option 1 is a trap."
    assert item.correct_why == "Option 0 is correct."
    assert item.correct_option.endswith("option 0")


@pytest.mark.django_db
def test_mistakes_are_grouped_by_lesson_and_ranked_most_missed_first(student, quiz):
    # The bank spreads questions across 4 lessons round-robin (12 questions ->
    # 3 per lesson). Getting everything wrong means every lesson appears with 3.
    result = _attempt(student, quiz, correct=0)
    fb = afe.analyse(result)

    assert fb.lesson_count == 4
    counts = [rl.mistakes for rl in fb.plan]
    assert counts == sorted(counts, reverse=True)   # ranked, most-missed first
    assert sum(counts) == fb.wrong_count


@pytest.mark.django_db
def test_the_plan_carries_the_lesson_coordinates_and_reading_time(student, quiz):
    result = _attempt(student, quiz, correct=0)
    fb = afe.analyse(result)
    top = fb.plan[0]
    assert top.module_order_index == quiz.module.order_index
    assert 1 <= top.lesson_number <= 4
    assert top.reading_time_minutes == 5


@pytest.mark.django_db
def test_blank_answers_are_not_itemised_but_still_count_against_the_score(student, quiz):
    # Answer the first 5 correctly, leave the rest blank: score 5/12, no wrongs.
    questions = list(quiz.questions.order_by("ordering").prefetch_related("answers"))
    ids = [q.id for q in questions]
    result, _, _ = svc.grade_and_record(
        student, quiz, ids, responses_for(questions[:5], correct=5)
    )
    fb = afe.analyse(result)
    assert result.passed is False
    assert fb.wrong_count == 0        # blanks record no WrongAnswer row


@pytest.mark.django_db
def test_analyse_is_a_single_query(student, quiz, django_assert_max_num_queries):
    result = _attempt(student, quiz, correct=2)
    with django_assert_max_num_queries(1):
        fb = afe.analyse(result)
        # touch everything the template reads
        [(i.your_why, i.correct_why, i.lesson_title, i.module_order_index) for i in fb.items]
        [(rl.title, rl.mistakes, rl.reading_time_minutes) for rl in fb.plan]
