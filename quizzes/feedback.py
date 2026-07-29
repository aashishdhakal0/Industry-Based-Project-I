"""The Adaptive Feedback Engine — turn a graded attempt into a study plan.

This is the product's differentiator. Instead of "you scored 60%", it reads the
WrongAnswer rows recorded at submit and produces, for each mistake: *why* the
chosen option was wrong and the right one right (from each option's
`explanation_text`), and *which lesson* teaches it (`lesson_reference`). It then
groups the mistakes by lesson into a ranked "revise these lessons" plan.

Pure and read-only. One query, everything the page needs prefetched — the AFE
runs on every result view, so it must not N+1.
"""

from dataclasses import dataclass

from .models import WrongAnswer


@dataclass
class FeedbackItem:
    """One wrong question, explained — your pick vs the right one, and the source."""

    question_text: str
    your_option: str
    your_why: str
    correct_option: str
    correct_why: str
    lesson_title: str
    module_order_index: int
    lesson_number: int


@dataclass
class RevisionLesson:
    """A lesson to revise, and how many of this attempt's mistakes trace to it."""

    title: str
    module_order_index: int
    lesson_number: int
    reading_time_minutes: int
    mistakes: int


@dataclass
class Feedback:
    items: list        # FeedbackItem, in question order
    plan: list         # RevisionLesson, most-missed first
    wrong_count: int
    lesson_count: int


def analyse(quiz_result):
    """Build the feedback + study plan for a recorded attempt.

    Reads the attempt's WrongAnswer rows (answered-wrong questions). A blank
    answer scores as wrong but records no row, so it isn't itemised here — the
    plan revises the lessons behind the mistakes the student actually made.
    """
    wrongs = (
        WrongAnswer.objects.filter(quiz_result=quiz_result)
        .select_related(
            "question",
            "question__lesson_reference",
            "question__lesson_reference__module",
            "student_answer",
            "correct_answer",
        )
        .order_by("question__ordering")
    )

    items = []
    by_lesson = {}  # lesson id -> [lesson, mistake_count]
    for wa in wrongs:
        lesson = wa.question.lesson_reference
        items.append(
            FeedbackItem(
                question_text=wa.question.question_text,
                your_option=wa.student_answer.option_text,
                your_why=wa.student_answer.explanation_text,
                correct_option=wa.correct_answer.option_text,
                correct_why=wa.correct_answer.explanation_text,
                lesson_title=lesson.title,
                module_order_index=lesson.module.order_index,
                lesson_number=lesson.lesson_number,
            )
        )
        entry = by_lesson.setdefault(lesson.id, [lesson, 0])
        entry[1] += 1

    plan = [
        RevisionLesson(
            title=lesson.title,
            module_order_index=lesson.module.order_index,
            lesson_number=lesson.lesson_number,
            reading_time_minutes=lesson.reading_time_minutes,
            mistakes=count,
        )
        # Most-missed lesson first; ties fall back to reading order.
        for lesson, count in sorted(
            by_lesson.values(),
            key=lambda e: (-e[1], e[0].module.order_index, e[0].lesson_number),
        )
    ]

    return Feedback(
        items=items,
        plan=plan,
        wrong_count=len(items),
        lesson_count=len(plan),
    )
