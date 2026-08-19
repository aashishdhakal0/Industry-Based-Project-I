"""The student learning experience: browse, module overview, lessons, simulation.

Every view here is behind login, and every view that serves module content
enforces the sequential lock *in the view* (a 403), never merely by hiding a
link — a hidden link is not a control (CLAUDE.md).
"""

import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from quizzes.models import QuizResult

from . import gamification as g
from .models import Lesson, LessonTask, Module, ProgressRecord
from .presentation import decorate

# Short, human labels + an icon for each task kind, shown as chips on the module
# overview. (label, sprite-icon id.)
_TASK_CHIP = {
    "CHECK": ("Check", "i-check-circle"),
    "CONCEPT": ("Read", "i-book"),
    "SCENARIO": ("Scenario", "i-branch"),
    "RESPOND": ("Decision", "i-branch"),
    "QUIZSET": ("Quiz set", "i-layers"),
    "SORT": ("Sort", "i-grid"),
    "CLASSIFY": ("Classify", "i-target"),
    "MAILSORT": ("Inbox", "i-mail"),
    "BRANCH": ("Branching", "i-branch"),
    "SEQUENCE": ("Order it", "i-layers"),
    "INBOX": ("Inbox", "i-mail"),
    "SPOT": ("Spot it", "i-eye"),
    "PASSWORD": ("Password", "i-lock"),
    "HARDEN": ("Harden", "i-shield"),
    "NETMAP": ("Network map", "i-grid"),
}


def _published_module(order_index):
    return get_object_or_404(Module, order_index=order_index, is_published=True)


def _locked_response(request, module):
    """A friendly 403 for a locked module. Returned (not raised) by content
    views when the user hasn't unlocked the module yet — real HTTP 403, so it's
    an enforced control, but a page a non-technical user can understand."""
    return render(request, "modules/locked.html", {"module": module}, status=403)


def _next_link(step, order_index):
    """Turn a within-module NextStep (from gamification.next_in_module) into the
    (url, label, kind) a page needs so the student always has one clear way
    forward: the next lesson, the quiz, or back to the now-complete module."""
    if step is None:
        return reverse("learn:module", args=[order_index]), "Finish module", "module"
    if step.kind == "quiz":
        return reverse("learn:quiz", args=[order_index]), "Take the quiz", "quiz"
    return (
        reverse("learn:lesson", args=[order_index, step.lesson.lesson_number]),
        "Next lesson",
        "lesson",
    )


@login_required
def browser(request):
    """The mission map — all published modules with real progress and lock state."""
    progress = g.module_progress(request.user)
    for mp in progress:
        decorate(mp.module)
        # The tile's state string and link, computed once here so the template
        # stays declarative. Locked tiles get no link.
        if not mp.unlocked:
            mp.state, mp.link = "locked", None
        else:
            if mp.complete:
                mp.state = "complete"
            elif mp.done_lessons > 0:
                mp.state = "current"
            else:
                mp.state = "open"
            mp.link = reverse("learn:module", args=[mp.module.order_index])
        mp.progress_label = f"{mp.done_lessons}/{mp.total_lessons}"

    step = g.next_step(request.user)
    profile = g.get_profile(request.user)

    return render(
        request,
        "modules/browser.html",
        {
            "progress": progress,
            "continue_module": step.module if step else None,
            "continue_lesson": step.lesson if step else None,
            "continue_kind": step.kind if step else None,
            "level": g.level_for_points(profile.points),
            "profile": profile,
            "modules_done": sum(1 for mp in progress if mp.complete),
            "modules_total": len(progress),
            "active": "modules",
        },
    )


@login_required
def module_overview(request, order_index):
    """A module's contents: its lessons (with done ticks), simulation and quiz."""
    module = _published_module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return _locked_response(request, module)

    # The no-JS celebration: a reward stashed by complete_lesson on redirect.
    reward_flash = request.session.pop("reward", None)

    lessons = list(module.lessons.filter(is_active=True).order_by("lesson_number"))
    done_numbers = set(
        ProgressRecord.objects.filter(
            user=request.user, lesson__module=module, lesson__is_active=True
        ).values_list("lesson__lesson_number", flat=True)
    )
    for lesson in lessons:
        lesson.is_done = lesson.lesson_number in done_numbers
        # Attach the lesson's tasks with per-task done state, so the overview can
        # show each lesson's contents as a roadmap.
        lesson.task_list = list(lesson.tasks.order_by("order"))
        if lesson.task_list:
            done_ids, _t, pdone, ptotal = g.lesson_task_stats(request.user, lesson)
            lesson.tasks_done = 0
            for t in lesson.task_list:
                t.done = t.id in done_ids
                label, icon = _TASK_CHIP.get(t.kind, ("Task", "i-check-circle"))
                t.chip_label = label
                t.chip_icon = icon
                t.chip_kind = t.kind.lower()
                if t.done:
                    lesson.tasks_done += 1
            lesson.tasks_total = len(lesson.task_list)

    simulation = getattr(module, "simulation", None)
    sim_done = (
        simulation is not None and simulation.results.filter(user=request.user).exists()
    )

    quiz = getattr(module, "quiz", None)
    if quiz is not None and not quiz.is_active:
        quiz = None
    quiz_passed = quiz is not None and QuizResult.objects.filter(
        user=request.user, quiz=quiz, passed=True
    ).exists()

    next_lesson = next((lesson for lesson in lessons if not lesson.is_done), None)
    all_lessons_done = bool(lessons) and next_lesson is None

    # Module complete = every lesson done and, if the module is gated by a quiz,
    # that quiz passed. This mirrors gamification.module_progress exactly, so the
    # celebration only fires when the next module has genuinely unlocked.
    module_complete = all_lessons_done and (quiz is None or quiz_passed)

    # The completion moment: the XP this module contributed, any badges the
    # student holds, and where to go next (the freshly unlocked module, or the
    # certificate if this was the last one).
    next_module = None
    module_points = 0
    earned_badges = []
    if module_complete:
        from .badges import BY_ID

        next_module = (
            Module.objects.filter(
                is_published=True, order_index=module.order_index + 1
            ).first()
        )
        module_points = len(done_numbers) * g.POINTS_PER_LESSON + (
            g.POINTS_PER_QUIZ if quiz_passed else 0
        )
        profile = g.get_profile(request.user)
        earned_badges = [BY_ID[b] for b in (profile.badges or []) if b in BY_ID]

    return render(
        request,
        "modules/overview.html",
        {
            "module": decorate(module),
            "lessons": lessons,
            "done_count": len(done_numbers),
            "total_count": len(lessons),
            "percent": round(len(done_numbers) / len(lessons) * 100) if lessons else 0,
            "simulation": simulation,
            "sim_done": sim_done,
            "quiz": quiz,
            "quiz_passed": quiz_passed,
            "next_lesson": next_lesson,
            "all_lessons_done": all_lessons_done,
            "module_complete": module_complete,
            "next_module": next_module,
            "module_points": module_points,
            "earned_badges": earned_badges,
            "reward_flash": reward_flash,
            # DEBUG-only: surface a link to the quiz-review preview page.
            "debug": settings.DEBUG,
            "active": "modules",
        },
    )


def _lesson_or_locked(request, order_index, lesson_number):
    """Fetch a lesson, enforcing publication, activity and the module lock.
    Returns (lesson, None) or (None, response)."""
    module = _published_module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return None, _locked_response(request, module)
    lesson = get_object_or_404(
        Lesson, module=module, lesson_number=lesson_number, is_active=True
    )
    return lesson, None


@login_required
def lesson(request, order_index, lesson_number):
    """The reading experience for one lesson."""
    lesson, blocked = _lesson_or_locked(request, order_index, lesson_number)
    if blocked:
        return blocked

    module = lesson.module
    siblings = list(module.lessons.filter(is_active=True).order_by("lesson_number"))
    numbers = [s.lesson_number for s in siblings]
    position = numbers.index(lesson.lesson_number)

    prev_lesson = siblings[position - 1] if position > 0 else None
    next_lesson = siblings[position + 1] if position < len(siblings) - 1 else None

    done_numbers = set(
        ProgressRecord.objects.filter(
            user=request.user, lesson__module=module, lesson__is_active=True
        ).values_list("lesson__lesson_number", flat=True)
    )
    is_done = lesson.lesson_number in done_numbers

    # The in-module stepper: one dot per lesson, marked done / current.
    steps = [
        {
            "number": s.lesson_number,
            "done": s.lesson_number in done_numbers,
            "current": s.lesson_number == lesson.lesson_number,
            "url": reverse("learn:lesson", args=[order_index, s.lesson_number]),
        }
        for s in siblings
    ]

    reward_flash = request.session.pop("reward", None)

    # Where "next" points once this lesson is done: the next lesson, the quiz if
    # this was the last one, or back to the (now complete) module. Computed as if
    # this lesson is already finished, so a completed lesson never dead-ends.
    after_step = g.next_in_module(
        request.user, module, also_done={lesson.lesson_number}
    )
    next_after_url, next_after_label, next_after_kind = _next_link(after_step, order_index)

    # Interactive task room (Module 1+). A lesson with tasks renders as a
    # TryHackMe-style sequence; lessons without tasks keep the plain reader.
    tasks = list(lesson.tasks.order_by("order"))
    lesson_points_done = lesson_points_total = 0
    if tasks:
        done_ids, _total, lesson_points_done, lesson_points_total = g.lesson_task_stats(
            request.user, lesson
        )
        current_marked = False
        for t in tasks:
            payload = t.payload or {}
            t.done = t.id in done_ids
            # The task index highlights the first unfinished task as "current".
            t.current = not t.done and not current_marked
            if t.current:
                current_marked = True
            t.options = payload.get("options", [])
            t.scenario = payload.get("scenario", "")
            t.question = payload.get("question", "")
            t.hint = payload.get("hint", "")
            t.inline_check = payload.get("inline_check")   # optional mid-panel check
            t.body2 = payload.get("body2", "")             # optional reading after it
            t.hero = payload.get("hero", "")               # optional top-of-panel figure

    return render(
        request,
        "modules/lesson.html",
        {
            "module": decorate(module),
            "lesson": lesson,
            "position": position + 1,
            "total": len(siblings),
            "progress_percent": round((position + 1) / len(siblings) * 100),
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "next_after_url": next_after_url,
            "next_after_label": next_after_label,
            "next_after_kind": next_after_kind,
            "is_done": is_done,
            "steps": steps,
            "tasks": tasks,
            "has_tasks": bool(tasks),
            "tasks_total": len(tasks),
            "tasks_done_count": sum(1 for t in tasks if getattr(t, "done", False)),
            "lesson_points_done": lesson_points_done,
            "lesson_points_total": lesson_points_total,
            "reward_flash": reward_flash,
            "active": "modules",
            # Focused, distraction-free room: the app shell drops the sidebar and
            # shows a slim focus bar with a clear way back to the module.
            "focus": True,
            "focus_back_url": reverse("learn:module", args=[order_index]),
            "focus_back_label": module.title,
            "focus_meta": f"Lesson {position + 1} of {len(siblings)}",
        },
    )


@login_required
@login_required
@require_POST
def complete_task(request, order_index, lesson_number):
    """Record one interactive task as done (fetch only). When it's the last task
    in the lesson, the engine banks the lesson and we return the celebration
    reward. Correctness is judged client-side for instant feedback; like
    mark-complete, this endpoint trusts that the task was done — these are
    formative, the graded assessment is the quiz."""
    lesson, blocked = _lesson_or_locked(request, order_index, lesson_number)
    if blocked:
        return blocked

    task = get_object_or_404(LessonTask, id=request.POST.get("task"), lesson=lesson)
    result = g.complete_task(request.user, task)

    # After this lesson (banked once its last task is done), the next thing to do:
    # the next lesson, the quiz, or back to the finished module.
    step = g.next_in_module(request.user, lesson.module, also_done={lesson_number})
    next_url, next_label, next_kind = _next_link(step, order_index)

    payload = {
        "task_points": result.task_points,
        "lesson_points_done": result.lesson_points_done,
        "lesson_points_total": result.lesson_points_total,
        "tasks_done": result.tasks_done,
        "tasks_total": result.tasks_total,
        "lesson_completed": result.lesson_completed,
        "next_url": next_url,
        "next_label": next_label,
        "module_done": step is None,
    }
    if result.lesson_completed and result.reward:
        r = result.reward
        payload["reward"] = {
            "points_gained": g.POINTS_PER_LESSON,
            "points": r.points,
            "level": r.level.level,
            "level_percent": r.level.percent,
            "streak": r.streak,
            "new_badges": [{"name": b.name, "icon": b.icon} for b in r.new_badges],
        }
    return JsonResponse(payload)


@require_POST
def complete_lesson(request, order_index, lesson_number):
    """Record a lesson as complete and award the points.

    Progressive enhancement: a plain form POST records and redirects to the next
    lesson (or the overview) with the reward in the session for a celebration
    banner. A `fetch` with the X-Requested-With header instead gets JSON back,
    so the JS can animate the reward inline without a page load. Same server
    path either way.
    """
    lesson, blocked = _lesson_or_locked(request, order_index, lesson_number)
    if blocked:
        return blocked

    created, reward = g.complete_lesson(request.user, lesson)

    # The lesson is now recorded done, so ask what's next in this module: the
    # next lesson, the quiz, or back to the finished module. Never a dead end.
    step = g.next_in_module(request.user, lesson.module)
    next_url, next_label, next_kind = _next_link(step, order_index)

    payload = {
        "created": created,
        "points": reward.points,
        "points_gained": g.POINTS_PER_LESSON if created else 0,
        "level": reward.level.level,
        "level_percent": reward.level.percent,
        "streak": reward.streak,
        "new_badges": [
            {"name": b.name, "icon": b.icon} for b in reward.new_badges
        ],
        "next_url": next_url,
        "next_label": next_label,
        "module_done": step is None,
    }

    if request.headers.get("X-Requested-With") == "fetch":
        return JsonResponse(payload)

    if created:
        request.session["reward"] = payload
    return redirect(next_url)


@login_required
def simulation(request, order_index):
    """The interactive simulation for a module."""
    module = _published_module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return _locked_response(request, module)

    sim = getattr(module, "simulation", None)
    if sim is None:
        return redirect("learn:module", order_index=order_index)

    previous = sim.results.filter(user=request.user).first()

    return render(
        request,
        "modules/simulation.html",
        {
            "module": decorate(module),
            "simulation": sim,
            # The scenario data as JSON for sim.js to drive the interaction.
            "scenario_json": json.dumps(sim.decision_points),
            "previous": previous,
            "active": "modules",
        },
    )


@login_required
@require_POST
def complete_simulation(request, order_index):
    """Record a simulation outcome (JSON body: score, total, path)."""
    module = _published_module(order_index)
    if not g.is_module_unlocked(request.user, module):
        return _locked_response(request, module)

    sim = getattr(module, "simulation", None)
    if sim is None:
        return JsonResponse({"error": "no simulation"}, status=404)

    try:
        data = json.loads(request.body or "{}")
        score = int(data.get("score", 0))
        total = int(data.get("total", 0))
        path = data.get("path", [])
        if not isinstance(path, list):
            raise ValueError
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "bad payload"}, status=400)

    # Clamp so a tampered client can't post score>total or negatives.
    total = max(0, total)
    score = max(0, min(score, total))

    reward = g.complete_simulation(
        request.user, sim, score=score, total=total, path=path
    )

    return JsonResponse(
        {
            "score": score,
            "total": total,
            "points": reward.points,
            "level": reward.level.level,
            "level_percent": reward.level.percent,
            "streak": reward.streak,
            "new_badges": [
                {"name": b.name, "icon": b.icon} for b in reward.new_badges
            ],
            "module_url": reverse("learn:module", args=[order_index]),
        }
    )


@login_required
def dashboard(request):
    """The student's home — every figure real, from PostgreSQL via the engine."""
    profile = g.get_profile(request.user)
    progress = g.module_progress(request.user)
    for mp in progress:
        decorate(mp.module)
        if not mp.unlocked:
            mp.state, mp.link = "locked", None
        else:
            mp.state = (
                "complete" if mp.complete
                else "current" if mp.done_lessons > 0
                else "open"
            )
            mp.link = reverse("learn:module", args=[mp.module.order_index])
        mp.progress_label = f"{mp.done_lessons}/{mp.total_lessons}"

    step = g.next_step(request.user)
    earned = set(profile.badges or [])

    # Recent activity — the last few lessons actually completed, newest first.
    recent = list(
        ProgressRecord.objects.filter(user=request.user)
        .select_related("lesson", "lesson__module")
        .order_by("-completed_at")[:4]
    )

    # Study calendar — the month the arrows point at, or this month by default.
    # Bad or missing params fall back to the current month rather than erroring.
    def _int_param(name):
        try:
            return int(request.GET.get(name))
        except (TypeError, ValueError):
            return None

    cal_year, cal_month = _int_param("cal_year"), _int_param("cal_month")
    if cal_month is not None and not 1 <= cal_month <= 12:
        cal_year = cal_month = None
    calendar = g.activity_calendar(request.user, year=cal_year, month=cal_month)

    # Mark the current stop for the roadmap: the first unlocked, unfinished
    # module (the one the student is on right now).
    current_index = step.module.order_index if step else None

    level = g.level_for_points(profile.points)
    tier = g.tier_for_points(profile.points)

    # One-time tier-up celebration: fire only when the student has genuinely
    # climbed past the highest tier we've congratulated them for, then record it
    # so it never repeats. Points only ever rise, so this can't fire falsely.
    celebrate_tier = None
    if tier.index > profile.celebrated_tier:
        celebrate_tier = tier.tier
        profile.celebrated_tier = tier.index
        profile.save(update_fields=["celebrated_tier"])

    stats = g.student_stats(request.user)
    lessons_done = stats["lessons_completed"]

    from .badges import CATALOGUE, nearest_unearned

    nearest = nearest_unearned(stats, earned)
    # Anticipation: a nearest-badge phrase if there is one, else next-level.
    if nearest:
        nudge_phrase = nearest[1]
        nudge_badge = nearest[0]
    else:
        nudge_phrase = f"Only {level.to_next} points to level {level.level + 1}"
        nudge_badge = None

    return render(
        request,
        "dashboard.html",
        {
            "active": "dashboard",
            "profile": profile,
            "greeting": g.greeting(),
            "rank": g.rank_for_level(level.level),
            "tier": tier,
            "tiers": g.TIERS,
            "celebrate_tier": celebrate_tier,
            "level": level,
            "streak": g.streak_status(profile),
            "progress": progress,
            "current_index": current_index,
            "modules_done": sum(1 for mp in progress if mp.complete),
            "modules_total": len(progress),
            # Roadmap geometry. Nodes = Start + N modules + Certified = N+2.
            # The connector fills to the last completed module: the fraction is
            # completed segments / total segments = modules_done / (nodes-1).
            "road_stops": len(progress) + 2,
            "road_fill": (
                round(sum(1 for mp in progress if mp.complete) / (len(progress) + 1) * 100)
                if progress else 0
            ),
            "lessons_done": lessons_done,
            "continue_module": step.module if step else None,
            "continue_lesson": step.lesson if step else None,
            "continue_kind": step.kind if step else None,
            "is_first_time": profile.points == 0 and lessons_done == 0,
            "recent": recent,
            "calendar": calendar,
            "nudge_phrase": nudge_phrase,
            "nudge_badge": nudge_badge,
            "badges": [{"badge": b, "earned": b.id in earned} for b in CATALOGUE],
            "badges_earned": len(earned),
            "badges_total": len(CATALOGUE),
        },
    )


@login_required
def progress(request):
    """My Progress — a per-module breakdown plus headline stats. Real data."""
    profile = g.get_profile(request.user)
    prog = g.module_progress(request.user)
    for mp in prog:
        decorate(mp.module)

    return render(
        request,
        "modules/progress.html",
        {
            "active": "progress",
            "profile": profile,
            "level": g.level_for_points(profile.points),
            "progress": prog,
            "lessons_done": sum(mp.done_lessons for mp in prog),
            "lessons_total": sum(mp.total_lessons for mp in prog),
            "modules_done": sum(1 for mp in prog if mp.complete),
            "modules_total": len(prog),
        },
    )


@login_required
def badges(request):
    """The achievement gallery — a collection to complete, grouped into tiers,
    earned vs locked from real data."""
    from .badges import CATALOGUE, grouped

    profile = g.get_profile(request.user)
    earned = set(profile.badges or [])
    return render(
        request,
        "modules/badges.html",
        {
            "active": "badges",
            "tiers": grouped(earned),
            "earned_count": len(earned),
            "total_count": len(CATALOGUE),
            "percent": round(len(earned) / len(CATALOGUE) * 100) if CATALOGUE else 0,
        },
    )


@login_required
def certificate(request):
    """The completion certificate — its on-screen design, plus a progress state.

    The real awarding (a Certificate row + a downloadable, verifiable PDF) lands
    with the quiz engine in Sprint 5. Here we render the certificate design
    populated with real data (name, the six modules), and show a progress
    preview until all modules are complete. The verification code is a clearly
    labelled sample — no fake "verified" claim.
    """
    import uuid

    from django.utils import timezone

    prog = g.module_progress(request.user)
    done = sum(1 for mp in prog if mp.complete)
    total = len(prog)
    earned = total > 0 and done >= total

    # Stable per-student sample code, so it looks like a real credential without
    # pretending to be one (the persistent UUID is issued with the PDF later).
    raw = uuid.uuid5(uuid.NAMESPACE_DNS, f"cybaroo-cert-{request.user.pk}").hex.upper()
    sample_code = f"CYB-{raw[:4]}-{raw[4:8]}-{raw[8:12]}"

    return render(
        request,
        "modules/certificate.html",
        {
            "active": "certificate",
            "modules": [
                {"title": mp.module.title, "complete": mp.complete} for mp in prog
            ],
            "modules_done": done,
            "modules_total": total,
            "percent": round(done / total * 100) if total else 0,
            "earned": earned,
            "student_name": request.user.get_full_name() or request.user.email,
            "issue_date": timezone.localdate(),
            "sample_code": sample_code,
        },
    )
