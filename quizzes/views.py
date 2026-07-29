"""Taking a quiz: the gate, the paper, save-as-you-go, submit, and the result.

The lock is enforced here, in the view, never only hidden in a template
(CLAUDE.md): a student may open a module's quiz only when the module is unlocked
and every lesson in it is done — learn first, then prove it. Grading and awarding
live in services.py; these views are the HTTP shell around it.
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from modules import gamification as g
from modules.models import Module, ProgressRecord

from . import services as svc
from .models import Answer, Question, Quiz, QuizResult

SESSION_KEY = "quiz_attempt"
REWARD_KEY = "quiz_reward"


def _module(order_index):
    return get_object_or_404(Module, order_index=order_index, is_published=True)


def _active_quiz(module):
    return get_object_or_404(Quiz, module=module, is_active=True)


def _all_lessons_done(user, module):
    total = module.lessons.filter(is_active=True).count()
    done = (
        ProgressRecord.objects.filter(
            user=user, lesson__module=module, lesson__is_active=True
        )
        .values("lesson")
        .distinct()
        .count()
    )
    return total > 0 and done >= total


def _load_questions(question_ids):
    """The presented questions, in the stored order, options attached."""
    by_id = {
        q.id: q
        for q in Question.objects.filter(id__in=question_ids).prefetch_related(
            Prefetch("answers", queryset=Answer.objects.order_by("id"))
        )
    }
    return [by_id[qid] for qid in question_ids if qid in by_id]


@login_required
def quiz(request, order_index):
    """Show the quiz paper. Draws ten questions on first open and holds the set
    (and any saved answers) in the session, so a refresh can't redraw or reset."""
    module = _module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return render(request, "modules/locked.html", {"module": module}, status=403)
    quiz = _active_quiz(module)
    if not _all_lessons_done(request.user, module):
        # Learn before you practise — send them back to finish the lessons.
        return redirect("learn:module", order_index=order_index)

    attempt = request.session.get(SESSION_KEY)
    if not (attempt and attempt.get("quiz_id") == quiz.id and attempt.get("question_ids")):
        drawn = svc.draw_questions(quiz)
        attempt = {
            "quiz_id": quiz.id,
            "question_ids": [q.id for q in drawn],
            "responses": {},
        }
        request.session[SESSION_KEY] = attempt

    questions = _load_questions(attempt["question_ids"])
    saved = attempt["responses"]
    for i, q in enumerate(questions, start=1):
        q.number = i
        q.saved = saved.get(str(q.id))

    return render(
        request,
        "quizzes/quiz.html",
        {
            "module": module,
            "quiz": quiz,
            "questions": questions,
            "total": len(questions),
            "active": "modules",
        },
    )


@login_required
def save_answer(request, order_index):
    """Persist a single answer as the student picks it (fetch, progressive
    enhancement). The form submit is still authoritative; this just means a
    refresh mid-quiz doesn't lose progress."""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    attempt = request.session.get(SESSION_KEY)
    if not attempt:
        return JsonResponse({"error": "no attempt in progress"}, status=409)
    try:
        qid = int(request.POST.get("question"))
        aid = int(request.POST.get("answer"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "bad payload"}, status=400)
    if qid not in attempt["question_ids"]:
        return JsonResponse({"error": "unknown question"}, status=400)
    attempt["responses"][str(qid)] = aid
    request.session.modified = True
    return JsonResponse({"saved": True})


@login_required
def submit_quiz(request, order_index):
    """Grade the attempt and move on to the result. The submitted form is the
    authoritative set of answers (its radios carry every choice); the session
    copy is only a resilience net."""
    module = _module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return render(request, "modules/locked.html", {"module": module}, status=403)
    quiz = _active_quiz(module)
    attempt = request.session.get(SESSION_KEY)
    if request.method != "POST" or not (attempt and attempt.get("quiz_id") == quiz.id):
        return redirect("learn:quiz", order_index=order_index)

    question_ids = attempt["question_ids"]
    responses = {}
    for qid in question_ids:
        raw = request.POST.get(f"q{qid}")
        if raw:
            try:
                responses[qid] = int(raw)
            except ValueError:
                pass

    # Was this quiz already passed? If so, passing again awards no fresh points
    # (points recompute from distinct passed quizzes) — so the result page can
    # honestly say "+50" only the first time.
    already_passed = QuizResult.objects.filter(
        user=request.user, quiz=quiz, passed=True
    ).exists()

    result, reward, _ = svc.grade_and_record(request.user, quiz, question_ids, responses)

    request.session.pop(SESSION_KEY, None)
    request.session[REWARD_KEY] = {
        "points": reward.points,
        "level": reward.level.level,
        "level_percent": reward.level.percent,
        "streak": reward.streak,
        "new_badges": [{"name": b.name, "icon": b.icon} for b in reward.new_badges],
        "awarded_points": g.POINTS_PER_QUIZ if result.passed and not already_passed else 0,
    }
    return redirect("learn:quiz_result", order_index=order_index)


@login_required
def quiz_result(request, order_index):
    """The result of the latest attempt — score, pass/fail, the reward moment,
    and the next step. The Adaptive Feedback Engine's breakdown is added here in
    the next slice."""
    module = _module(order_index)
    quiz = _active_quiz(module)
    result = (
        QuizResult.objects.filter(user=request.user, quiz=quiz)
        .order_by("-attempt_number")
        .first()
    )
    if not result:
        return redirect("learn:quiz", order_index=order_index)

    reward = request.session.pop(REWARD_KEY, None)
    next_module = Module.objects.filter(
        is_published=True, order_index=module.order_index + 1
    ).first()
    return render(
        request,
        "quizzes/result.html",
        {
            "module": module,
            "quiz": quiz,
            "result": result,
            "passed": result.passed,
            "reward": reward,
            "next_module": next_module,
            "active": "modules",
        },
    )
