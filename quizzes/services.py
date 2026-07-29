"""The quiz engine's write path: draw a paper, grade it, record the result.

Same rule as the gamification engine — **records are the truth**. A QuizResult
and its WrongAnswers are the durable record of an attempt; points and the quiz
badges are *recomputed* from them by `refresh_profile`, never incremented here,
so a retake that passes again can't inflate anything.

Grading never trusts the client for correctness: the chosen answer ids are
looked up against the question's own options loaded from the database, and the
score is computed server-side against the stored `correct_answer` flag.
"""

from dataclasses import dataclass

from django.db import transaction
from django.db.models import Max, Prefetch

from modules import gamification as g

from .models import Answer, Question, QuizResult, WrongAnswer

QUESTIONS_PER_ATTEMPT = 10


def draw_questions(quiz, n=QUESTIONS_PER_ATTEMPT):
    """Draw up to `n` questions at random from the quiz's bank, options attached.

    `order_by('?')` is DB-side (``ORDER BY RANDOM()``) and then sliced, so it
    never pulls the whole bank into Python — the trap CLAUDE.md warns about with
    ``random.sample()`` on a queryset.
    """
    return list(
        quiz.questions.prefetch_related(
            Prefetch("answers", queryset=Answer.objects.order_by("id"))
        ).order_by("?")[:n]
    )


@dataclass
class GradedQuestion:
    """One graded line of an attempt — the unit the results page and AFE read."""

    question: Question
    chosen: Answer | None      # None when the student left it blank
    correct: Answer | None
    is_correct: bool
    answered: bool


def _grade(questions, responses):
    """Grade the presented questions against the student's responses.

    `responses` maps question id -> chosen answer id (or None). Returns the list
    of GradedQuestion in the order the questions were presented.
    """
    graded = []
    for q in questions:
        options = {a.id: a for a in q.answers.all()}
        correct = next((a for a in q.answers.all() if a.correct_answer), None)
        chosen_id = responses.get(q.id)
        chosen = options.get(chosen_id) if chosen_id is not None else None
        is_correct = chosen is not None and chosen.correct_answer
        graded.append(
            GradedQuestion(
                question=q,
                chosen=chosen,
                correct=correct,
                is_correct=is_correct,
                answered=chosen is not None,
            )
        )
    return graded


def score_of(graded):
    """Percentage correct over everything presented (blanks count against)."""
    total = len(graded)
    if not total:
        return 0
    return round(sum(1 for gq in graded if gq.is_correct) / total * 100)


@transaction.atomic
def grade_and_record(user, quiz, question_ids, responses, *, today=None, now=None):
    """Grade an attempt over the presented questions and record it.

    `question_ids` is the exact set that was shown (held in the session so a
    refresh can't redraw a different paper); `responses` maps question id ->
    chosen answer id (or None). Returns ``(quiz_result, reward, graded)``.

    The reward comes from the gamification engine recomputing from truth: on a
    pass, distinct passed-quiz count rises and the +50 and quiz badges follow.
    """
    presented = {
        q.id: q
        for q in Question.objects.filter(id__in=question_ids, quiz=quiz)
        .select_related("lesson_reference")
        .prefetch_related(Prefetch("answers", queryset=Answer.objects.order_by("id")))
    }
    # Preserve the order the questions were shown in.
    questions = [presented[qid] for qid in question_ids if qid in presented]
    graded = _grade(questions, responses)

    score = score_of(graded)
    passed = score >= quiz.pass_mark
    attempt_number = (
        QuizResult.objects.filter(user=user, quiz=quiz).aggregate(
            m=Max("attempt_number")
        )["m"]
        or 0
    ) + 1

    result = QuizResult.objects.create(
        user=user,
        quiz=quiz,
        score=score,
        passed=passed,
        attempt_number=attempt_number,
    )
    # One WrongAnswer per answered-but-wrong question — the AFE's durable input.
    # Blanks score as wrong but have no chosen option to record.
    WrongAnswer.objects.bulk_create(
        [
            WrongAnswer(
                quiz_result=result,
                question=gq.question,
                student_answer=gq.chosen,
                correct_answer=gq.correct,
            )
            for gq in graded
            if gq.answered and not gq.is_correct and gq.correct is not None
        ]
    )

    reward = g.refresh_profile(user, bump_streak=True, today=today, now=now)
    return result, reward, graded
