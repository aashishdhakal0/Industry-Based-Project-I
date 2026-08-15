"""The quiz engine's write path: drawing, grading, recording, awarding, unlocking.

The theme mirrors the gamification tests: the QuizResult/WrongAnswer records are
the truth, and points can't drift or double-count across retakes.
"""

import pytest

from modules import gamification as g
from quizzes import services as svc
from quizzes.models import QuizResult, WrongAnswer

from .conftest import responses_for


# --------------------------------------------------------------------------
# Drawing the paper
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_draw_returns_ten_questions_from_the_bank(quiz):
    drawn = svc.draw_questions(quiz)
    assert len(drawn) == 10
    assert all(q.quiz_id == quiz.id for q in drawn)


@pytest.mark.django_db
def test_draw_is_a_bounded_number_of_queries(quiz, django_assert_max_num_queries):
    # The random draw plus one prefetch of options — never one query per question.
    with django_assert_max_num_queries(2):
        drawn = svc.draw_questions(quiz)
        [list(q.answers.all()) for q in drawn]


@pytest.mark.django_db
def test_a_small_bank_draws_all_it_has(make_module, author):
    from quizzes.models import Quiz

    m = make_module(2)
    small = Quiz.objects.create(module=m, pass_mark=70)
    from quizzes.tests.conftest import _build_bank

    _build_bank(small, size=6)
    assert len(svc.draw_questions(small)) == 6


# --------------------------------------------------------------------------
# Grading + recording
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_a_perfect_paper_passes_scores_100_and_records_no_wrong_answers(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    result, reward, graded = svc.grade_and_record(
        student, quiz, ids, responses_for(drawn, correct=10)
    )
    assert result.score == 100 and result.passed is True
    assert WrongAnswer.objects.filter(quiz_result=result).count() == 0
    assert all(gq.is_correct for gq in graded)


@pytest.mark.django_db
def test_seventy_percent_is_a_pass_at_the_boundary(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    result, _, _ = svc.grade_and_record(student, quiz, ids, responses_for(drawn, correct=7))
    assert result.score == 70 and result.passed is True


@pytest.mark.django_db
def test_below_the_mark_fails_and_records_each_wrong_answer(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    result, reward, _ = svc.grade_and_record(
        student, quiz, ids, responses_for(drawn, correct=6)
    )
    assert result.score == 60 and result.passed is False
    assert WrongAnswer.objects.filter(quiz_result=result).count() == 4


@pytest.mark.django_db
def test_a_wrong_answer_links_the_chosen_and_the_correct_option(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    result, _, _ = svc.grade_and_record(student, quiz, ids, responses_for(drawn, correct=9))
    wa = WrongAnswer.objects.filter(quiz_result=result).select_related(
        "student_answer", "correct_answer"
    ).get()
    assert wa.student_answer.correct_answer is False
    assert wa.correct_answer.correct_answer is True


@pytest.mark.django_db
def test_blank_answers_count_against_the_score_but_record_no_wrong_answer(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    # Answer the first six correctly, leave the last four blank.
    responses = responses_for(drawn[:6], correct=6)
    result, _, graded = svc.grade_and_record(student, quiz, ids, responses)
    assert result.score == 60 and result.passed is False
    # Blanks are wrong but have no chosen option, so no WrongAnswer rows for them.
    assert WrongAnswer.objects.filter(quiz_result=result).count() == 0
    assert sum(1 for gq in graded if not gq.answered) == 4


# --------------------------------------------------------------------------
# Awarding — through the gamification engine, from truth
# --------------------------------------------------------------------------


@pytest.mark.django_db
def test_passing_awards_the_quiz_points_and_badge(student, quiz):
    drawn = svc.draw_questions(quiz)
    result, reward, _ = svc.grade_and_record(
        student, quiz, [q.id for q in drawn], responses_for(drawn, correct=10)
    )
    assert reward.points == g.POINTS_PER_QUIZ        # one passed quiz, no lessons
    assert "first_quiz" in [b.id for b in reward.new_badges]


@pytest.mark.django_db
def test_failing_awards_nothing(student, quiz):
    drawn = svc.draw_questions(quiz)
    _, reward, _ = svc.grade_and_record(
        student, quiz, [q.id for q in drawn], responses_for(drawn, correct=5)
    )
    assert reward.points == 0
    assert g.get_profile(student).points == 0


@pytest.mark.django_db
def test_retaking_and_passing_again_does_not_double_the_points(student, quiz):
    drawn = svc.draw_questions(quiz)
    ids = [q.id for q in drawn]
    first, _, _ = svc.grade_and_record(student, quiz, ids, responses_for(drawn, correct=10))
    second, reward, _ = svc.grade_and_record(student, quiz, ids, responses_for(drawn, correct=10))

    assert second.attempt_number == first.attempt_number + 1
    assert reward.points == g.POINTS_PER_QUIZ        # still one distinct passed quiz
    assert QuizResult.objects.filter(user=student, passed=True).count() == 2


# --------------------------------------------------------------------------
# Unlocking — a passed quiz is what opens the next module
# --------------------------------------------------------------------------


def _finish_lessons(student, module):
    for lesson in module.lessons.order_by("lesson_number"):
        g.complete_lesson(student, lesson)


@pytest.mark.django_db
def test_finishing_lessons_alone_does_not_complete_a_quiz_gated_module(
    student, quiz, make_module
):
    make_module(2)  # a next module to unlock
    _finish_lessons(student, quiz.module)

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[1].complete is False   # lessons done, quiz still pending
    assert progress[2].unlocked is False   # so module 2 stays locked


@pytest.mark.django_db
def test_passing_the_quiz_completes_the_module_and_unlocks_the_next(
    student, quiz, make_module
):
    make_module(2)
    _finish_lessons(student, quiz.module)
    drawn = svc.draw_questions(quiz)
    svc.grade_and_record(student, quiz, [q.id for q in drawn], responses_for(drawn, correct=10))

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[1].complete is True
    assert progress[2].unlocked is True


@pytest.mark.django_db
def test_failing_the_quiz_leaves_the_next_module_locked(student, quiz, make_module):
    make_module(2)
    _finish_lessons(student, quiz.module)
    drawn = svc.draw_questions(quiz)
    svc.grade_and_record(student, quiz, [q.id for q in drawn], responses_for(drawn, correct=4))

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[1].complete is False
    assert progress[2].unlocked is False


@pytest.mark.django_db
def test_a_module_without_a_quiz_still_completes_on_lessons_alone(student, make_module):
    m = make_module(1)          # no Quiz created for it
    make_module(2)
    _finish_lessons(student, m)

    progress = {mp.module.order_index: mp for mp in g.module_progress(student)}
    assert progress[1].complete is True
    assert progress[2].unlocked is True
