"""Administrator dashboard: overview, learner list, CSV export.

Every view is behind administrator_required — a real 403 for anyone who isn't
an Administrator, not merely a hidden sidebar link.
"""

import csv

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from authentication.decorators import administrator_required
from authentication.models import User
from modules.models import Lesson, Module
from quizzes.models import Question, Quiz

from . import services
from .forms import AddUserForm, LessonEditForm, ModuleEditForm, QuestionEditForm
from .models import AdminAction

PER_PAGE = 25


def _render(request, template, context):
    """Render a console page. `console=True` scopes the calm admin theme and
    loads admin.js (see staff/base.html and the .cy-app--console CSS)."""
    context.setdefault("console", True)
    return render(request, template, context)


@administrator_required
def overview(request):
    """Welcome + headline stats + grade-tier distribution + admin activity."""
    from modules import gamification as g

    rows = services.collect_learners()
    stats = services.overview(rows)
    return _render(
        request,
        "staff/overview.html",
        {
            "active": "admin_overview",
            "stats": stats,
            "greeting": g.greeting(),
            "recent_actions": services.recent_actions(),
            "content_health": services.content_health(),
        },
    )


@administrator_required
def learners(request):
    """The learner table: search, quick-filter, sort, paginate.

    All four operate on the rows from one collect_learners() call, so the
    bounded-query aggregation is preserved — no N+1 as the cohort grows.
    """
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", services.DEFAULT_SORT)
    if sort not in services.SORTS:
        sort = services.DEFAULT_SORT
    filter_key = request.GET.get("filter", "")
    if filter_key not in services.QUICK_FILTERS:
        filter_key = ""

    rows = services.collect_learners()
    total_all = len(rows)
    rows = services.search_learners(rows, q)
    if filter_key:
        rows = services.filter_learners(rows, filter_key)
    rows = services.sort_and_filter(rows, sort=sort)
    match_count = len(rows)

    page_obj = Paginator(rows, PER_PAGE).get_page(request.GET.get("page"))

    # Base querystring (minus page) so pagination + row links keep the view.
    params = request.GET.copy()
    params.pop("page", None)
    base_qs = params.urlencode()

    return _render(
        request,
        "staff/learners.html",
        {
            "active": "admin_learners",
            "page_obj": page_obj,
            "rows": page_obj.object_list,
            "match_count": match_count,
            "total_all": total_all,
            "sort": sort,
            "q": q,
            "filter": filter_key,
            "status_chips": [(k, services.QUICK_FILTERS[k][0]) for k in services.STATUS_FILTER_KEYS],
            "grade_chips": [(k, services.QUICK_FILTERS[k][0]) for k in services.GRADE_FILTER_KEYS],
            "base_qs": base_qs,
        },
    )


@administrator_required
def organisations(request):
    """Learners grouped by organisation, with aggregate stats."""
    rows = services.collect_learners()
    return _render(
        request,
        "staff/organisations.html",
        {
            "active": "admin_orgs",
            "orgs": services.organisation_rollup(rows),
            "total_learners": len(rows),
        },
    )


@administrator_required
def activity(request):
    """The full admin audit trail, newest first, paginated."""
    qs = AdminAction.objects.select_related("actor", "target_user")
    page_obj = Paginator(qs, 40).get_page(request.GET.get("page"))
    return _render(
        request,
        "staff/activity.html",
        {"active": "admin_activity", "page_obj": page_obj, "actions": page_obj.object_list},
    )


@administrator_required
def learners_csv(request):
    """Download the learner progress report as CSV."""
    rows = services.sort_and_filter(services.collect_learners())

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="cybaroo-learner-progress.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Name",
            "Email",
            "Organisation",
            "Modules completed",
            "Modules total",
            "Overall score",
            "Grade",
            "Points",
            "Last active",
        ]
    )
    for r in rows:
        profile = getattr(r.user, "profile", None)
        writer.writerow(
            [
                r.name,
                r.user.email,
                profile.organisation if profile else "",
                r.modules_completed,
                r.modules_total,
                "" if r.overall_score is None else r.overall_score,
                r.tier.name,
                r.points,
                r.last_active.strftime("%Y-%m-%d %H:%M") if r.last_active else "",
            ]
        )
    return response


@administrator_required
def learner_detail(request, user_id):
    """The full picture of one learner, and the actions an admin can take."""
    learner = get_object_or_404(
        User.objects.select_related("profile"), pk=user_id
    )
    # Preserve the list's search/filter/sort so "back" returns to the same view.
    back = request.GET.get("back", "")
    back_url = reverse("staff:learners") + (f"?{back}" if back else "")

    context = services.learner_detail(learner)
    context.update(
        {
            "active": "admin_learners",
            "roles": User.Role.choices,
            "actions": AdminAction.objects.filter(target_user=learner)[:8],
            "back_url": back_url,
        }
    )
    return _render(request, "staff/learner_detail.html", context)


@administrator_required
def user_new(request):
    """Create a new account (staff or student) and assign its role."""
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            services.log_action(
                request.user,
                AdminAction.Kind.ADD_USER,
                f"Added {user.email} as {user.get_role_display()}",
                target_user=user,
            )
            messages.success(
                request, f"Created {user.email} ({user.get_role_display()})."
            )
            return redirect("staff:learner_detail", user_id=user.pk)
    else:
        form = AddUserForm()

    return _render(
        request, "staff/user_new.html", {"active": "admin_learners", "form": form}
    )


@administrator_required
def content(request):
    """A read view of every module and its lessons, with publish status."""
    modules = list(
        Module.objects.annotate(
            total_lessons=Count("lessons", distinct=True),
            active_lessons=Count(
                "lessons", filter=Q(lessons__is_active=True), distinct=True
            ),
        ).order_by("order_index")
    )
    has_quiz = set(
        Module.objects.filter(quiz__isnull=False).values_list("id", flat=True)
    )
    for m in modules:
        m.has_quiz = m.id in has_quiz
    return _render(
        request,
        "staff/content.html",
        {"active": "admin_content", "modules": modules},
    )


@administrator_required
@require_POST
def content_publish(request, order_index):
    """Publish or unpublish a module (soft-delete via is_published)."""
    module = get_object_or_404(Module, order_index=order_index)
    module.is_published = not module.is_published
    module.save(update_fields=["is_published"])

    kind = AdminAction.Kind.PUBLISH if module.is_published else AdminAction.Kind.UNPUBLISH
    verb = "Published" if module.is_published else "Unpublished"
    services.log_action(request.user, kind, f"{verb} “{module.title}”")
    messages.success(request, f"{verb} “{module.title}”.")
    return redirect("staff:content")


@administrator_required
def module_detail(request, order_index):
    """View and edit one module: its own fields, its lessons, its quiz."""
    module = get_object_or_404(Module, order_index=order_index)

    if request.method == "POST":
        form = ModuleEditForm(request.POST, instance=module)
        if form.is_valid():
            module = form.save(commit=False)
            module.admin_edited = True  # lock against a reseed overwrite
            module.save()
            services.log_action(
                request.user,
                AdminAction.Kind.EDIT_MODULE,
                f"Edited module “{module.title}”",
            )
            messages.success(request, f"Saved changes to “{module.title}”.")
            return redirect("staff:module_detail", order_index=module.order_index)
    else:
        form = ModuleEditForm(instance=module)

    quiz = Quiz.objects.filter(module=module).first()
    return _render(
        request,
        "staff/module_detail.html",
        {
            "active": "admin_content",
            "module": module,
            "form": form,
            "lessons": module.lessons.order_by("lesson_number"),
            "quiz": quiz,
            "question_count": quiz.questions.count() if quiz else 0,
        },
    )


@administrator_required
def lesson_edit(request, lesson_id):
    """Edit a lesson's title, reading time and (sanitised) body HTML."""
    lesson = get_object_or_404(Lesson.objects.select_related("module"), pk=lesson_id)

    if request.method == "POST":
        form = LessonEditForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.admin_edited = True  # lock against a reseed overwrite
            lesson.save()  # Lesson.save() runs nh3 over body_text.
            services.log_action(
                request.user,
                AdminAction.Kind.EDIT_LESSON,
                f"Edited lesson “{lesson.title}” in “{lesson.module.title}”",
            )
            messages.success(request, "Saved lesson changes.")
            return redirect("staff:lesson_edit", lesson_id=lesson.pk)
    else:
        form = LessonEditForm(instance=lesson)

    return _render(
        request,
        "staff/lesson_edit.html",
        {
            "active": "admin_content",
            "lesson": lesson,
            "module": lesson.module,
            "form": form,
            "tasks": lesson.tasks.order_by("order"),
        },
    )


@administrator_required
@require_POST
def lesson_publish(request, lesson_id):
    """Publish or unpublish a single lesson (soft delete via is_active)."""
    lesson = get_object_or_404(Lesson.objects.select_related("module"), pk=lesson_id)
    lesson.is_active = not lesson.is_active
    lesson.save(update_fields=["is_active"])

    if lesson.is_active:
        kind, verb = AdminAction.Kind.PUBLISH_LESSON, "Published"
    else:
        kind, verb = AdminAction.Kind.UNPUBLISH_LESSON, "Unpublished"
    services.log_action(
        request.user, kind, f"{verb} lesson “{lesson.title}” in “{lesson.module.title}”"
    )
    messages.success(request, f"{verb} “{lesson.title}”.")
    return redirect("staff:module_detail", order_index=lesson.module.order_index)


@administrator_required
def quiz_view(request, order_index):
    """Read view of a module's quiz: every question, its options, explanations."""
    module = get_object_or_404(Module, order_index=order_index)
    quiz = get_object_or_404(Quiz, module=module)
    questions = (
        quiz.questions.prefetch_related("answers")
        .select_related("lesson_reference")
        .order_by("ordering", "id")
    )
    return _render(
        request,
        "staff/quiz_view.html",
        {
            "active": "admin_content",
            "module": module,
            "quiz": quiz,
            "questions": questions,
        },
    )


@administrator_required
def question_edit(request, question_id):
    """Edit one question: its text, four options, the correct one, explanations."""
    question = get_object_or_404(
        Question.objects.select_related("quiz__module"), pk=question_id
    )

    if request.method == "POST":
        form = QuestionEditForm(request.POST, question=question)
        if form.is_valid():
            form.save()
            services.log_action(
                request.user,
                AdminAction.Kind.EDIT_QUESTION,
                f"Edited a question in the “{question.quiz.module.title}” quiz",
            )
            messages.success(request, "Saved question changes.")
            return redirect(
                "staff:quiz_view", order_index=question.quiz.module.order_index
            )
    else:
        form = QuestionEditForm(question=question)

    return _render(
        request,
        "staff/question_edit.html",
        {
            "active": "admin_content",
            "question": question,
            "module": question.quiz.module,
            "form": form,
        },
    )
