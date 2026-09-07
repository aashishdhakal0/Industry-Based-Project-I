"""Administrator dashboard: overview, learner list, CSV export.

Every view is behind administrator_required — a real 403 for anyone who isn't
an Administrator, not merely a hidden sidebar link.
"""

import csv
import datetime

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from authentication.decorators import administrator_required
from authentication.models import Organisation, User
from modules.models import Lesson, Module
from quizzes.models import Question, Quiz

from . import services
from .forms import (
    AddUserForm,
    LessonEditForm,
    ModuleEditForm,
    OrganisationForm,
    QuestionEditForm,
)
from .models import AdminAction

PER_PAGE = 25


def _render(request, template, context):
    """Render a console page. `console=True` scopes the admin theme and loads
    admin.js; `console_theme` carries the admin's remembered light/dark choice so
    the shell renders it on load (no flash of the wrong theme)."""
    context.setdefault("console", True)
    profile = getattr(request.user, "profile", None)
    context.setdefault("console_theme", getattr(profile, "console_theme", "dark") or "dark")
    return render(request, template, context)


@administrator_required
@require_POST
def set_theme(request):
    """Remember an administrator's light/dark choice. Progressive enhancement:
    a plain POST redirects back (no-JS); admin.js posts it via fetch and flips the
    theme instantly. Not audited — it's a personal display preference, not an act
    on another account or on content."""
    profile = getattr(request.user, "profile", None)
    if profile is None:
        from authentication.models import UserProfile

        profile = UserProfile.objects.create(user=request.user)

    theme = request.POST.get("theme")
    if theme not in ("dark", "light"):
        # No explicit value → flip the current one.
        theme = "light" if profile.console_theme == "dark" else "dark"
    profile.console_theme = theme
    profile.save(update_fields=["console_theme"])

    if request.headers.get("X-Requested-With") == "fetch":
        return HttpResponse(status=204)
    nxt = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("staff:overview")
    return redirect(nxt)


@administrator_required
def overview(request):
    """Welcome + headline stats + grade-tier distribution + admin activity."""
    from modules import gamification as g

    rows = services.collect_learners()
    stats = services.overview(rows)

    def _int(name):
        try:
            return int(request.GET.get(name))
        except (TypeError, ValueError):
            return None

    cal_month = _int("cal_month")
    if cal_month is not None and not 1 <= cal_month <= 12:
        cal_month = None
    calendar = services.admin_calendar(year=_int("cal_year"), month=cal_month)

    return _render(
        request,
        "staff/overview.html",
        {
            "active": "admin_overview",
            "stats": stats,
            "period": services.period_metrics(),
            "cohorts": services.attention_cohorts(rows),
            "greeting": g.greeting(),
            "recent_actions": services.recent_actions(),
            "content_health": services.content_health(),
            "calendar": calendar,
        },
    )


@administrator_required
def learners(request):
    """The learners page, in two shapes over one bounded aggregation:

    - "grouped" (default): people grouped into their organisation, students AND
      administrators, each org a collapsible section with quick stats.
    - "list": the flat, sortable, paginated table (students only).

    Search and quick-filters apply to both; no N+1 as the cohort grows.
    """
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", services.DEFAULT_SORT)
    if sort not in services.SORTS:
        sort = services.DEFAULT_SORT
    filter_key = request.GET.get("filter", "")
    if filter_key not in services.QUICK_FILTERS:
        filter_key = ""
    view = request.GET.get("view", "grouped")
    if view not in ("grouped", "list"):
        view = "grouped"

    if view == "grouped":
        roles = (User.Role.STUDENT, User.Role.INSTRUCTOR, User.Role.ADMINISTRATOR)
        rows = services.collect_learners(roles=roles)
    else:
        rows = services.collect_learners()   # students only
    total_all = len(rows)
    rows = services.search_learners(rows, q)
    if filter_key:
        rows = services.filter_learners(rows, filter_key)
    match_count = len(rows)

    groups = page_obj = None
    if view == "grouped":
        groups = services.group_by_organisation(rows)
    else:
        rows = services.sort_and_filter(rows, sort=sort)
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
            "view": view,
            "groups": groups,
            "page_obj": page_obj,
            "rows": page_obj.object_list if page_obj else [],
            "match_count": match_count,
            "total_all": total_all,
            "sort": sort,
            "q": q,
            "filter": filter_key,
            "status_chips": [(k, services.QUICK_FILTERS[k][0]) for k in services.STATUS_FILTER_KEYS],
            "grade_chips": [(k, services.QUICK_FILTERS[k][0]) for k in services.GRADE_FILTER_KEYS],
            "base_qs": base_qs,
            "organisations": Organisation.objects.all(),
        },
    )


@administrator_required
def organisations(request):
    """Managed organisations, each with its learner stats. Create + drill in."""
    orgs = services.managed_organisations()
    return _render(
        request,
        "staff/organisations.html",
        {
            "active": "admin_orgs",
            "orgs": orgs,
            "total_orgs": len(orgs),
            "total_learners": sum(o["learners"] for o in orgs),
            "unassigned_count": len(services.unassigned_members()),
        },
    )


@administrator_required
def unassigned(request):
    """The 'No organisation' group — everyone (students + staff) with no org."""
    members = services.unassigned_members()
    return _render(
        request,
        "staff/unassigned.html",
        {"active": "admin_orgs", "members": members},
    )


@administrator_required
def org_new(request):
    """Create a new organisation."""
    if request.method == "POST":
        form = OrganisationForm(request.POST)
        if form.is_valid():
            org = form.save()
            services.log_action(
                request.user, AdminAction.Kind.CREATE_ORG,
                f"Created organisation “{org.name}”",
            )
            messages.success(request, f"Created “{org.name}”.")
            return redirect("staff:org_detail", org_id=org.pk)
    else:
        form = OrganisationForm()
    return _render(
        request, "staff/org_new.html", {"active": "admin_orgs", "form": form}
    )


@administrator_required
def org_detail(request, org_id):
    """One organisation: its details (editable) and its members."""
    org = get_object_or_404(Organisation, pk=org_id)

    if request.method == "POST":
        form = OrganisationForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save()
            services.log_action(
                request.user, AdminAction.Kind.EDIT_ORG,
                f"Edited organisation “{org.name}”",
            )
            messages.success(request, "Saved organisation details.")
            return redirect("staff:org_detail", org_id=org.pk)
    else:
        form = OrganisationForm(instance=org)

    members = services.organisation_members(org)
    students = [m for m in members if m.is_student]
    completed = sum(1 for m in students if m.completed_course)
    from django.utils import timezone

    overdue = bool(
        org.training_due
        and org.training_due < timezone.localdate()
        and completed < len(students)
    )
    return _render(
        request,
        "staff/org_detail.html",
        {
            "active": "admin_orgs",
            "org": org,
            "form": form,
            "members": members,
            "student_count": len(students),
            "overdue": overdue,
        },
    )


@administrator_required
def activity(request):
    """The full admin audit trail: newest first, filterable, searchable, paginated."""
    qs, active_filters = services.filter_admin_actions(request.GET)
    total = qs.count()
    page_obj = Paginator(qs, 40).get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    base_qs = params.urlencode()

    return _render(
        request,
        "staff/activity.html",
        {
            "active": "admin_activity",
            "page_obj": page_obj,
            "actions": page_obj.object_list,
            "filters": active_filters,
            "any_filter": any(active_filters.values()),
            "match_count": total,
            "actors": services.audit_actors(),
            "kinds": AdminAction.Kind.choices,
            "base_qs": base_qs,
        },
    )


@administrator_required
def activity_csv(request):
    """Download the audit log (respecting the current filters) as CSV."""
    qs, _ = services.filter_admin_actions(request.GET)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="cybaroo-audit-log.csv"'
    writer = csv.writer(response)
    writer.writerow(["When", "Administrator", "Action", "Affected account", "Detail"])
    for a in qs.iterator():
        writer.writerow(
            [
                a.created_at.strftime("%Y-%m-%d %H:%M"),
                a.actor.email if a.actor else "(removed)",
                a.get_action_display(),
                a.target_user.email if a.target_user else "",
                a.summary,
            ]
        )
    return response


def _parse_date(raw):
    import datetime as _dt

    try:
        return _dt.date.fromisoformat((raw or "").strip())
    except (ValueError, TypeError):
        return None


@administrator_required
def reports(request):
    """The reporting hub: the exports and summaries a compliance officer needs."""
    from certificates.models import Certificate

    return _render(
        request,
        "staff/reports.html",
        {
            "active": "admin_reports",
            "learner_count": User.objects.filter(role=User.Role.STUDENT).count(),
            "org_count": Organisation.objects.count(),
            "cert_count": Certificate.objects.count(),
            "organisations": Organisation.objects.all(),
        },
    )


@administrator_required
def report_compliance(request):
    """Compliance summary as at a chosen date, optionally scoped to one org.
    On-screen, or CSV with ?format=csv (same filters)."""
    from django.utils import timezone

    date = _parse_date(request.GET.get("as_at"))
    as_at = None
    if date is not None:
        # Count everything up to the end of the chosen day.
        as_at = timezone.make_aware(datetime.datetime.combine(date, datetime.time.max))
    org_id = (request.GET.get("org") or "").strip()
    org = Organisation.objects.filter(pk=org_id).first() if org_id.isdigit() else None

    report = services.compliance_report(as_at=as_at, org=org)

    if request.GET.get("format") == "csv":
        response = HttpResponse(content_type="text/csv")
        label = (org.name.lower().replace(" ", "-") + "-") if org else ""
        response["Content-Disposition"] = f'attachment; filename="cybaroo-{label}compliance.csv"'
        writer = csv.writer(response)
        writer.writerow(["As at", date.isoformat() if date else "today"])
        writer.writerow(["Name", "Email", "Organisation", "Modules completed",
                         "Modules total", "Completed course"])
        for r in report["rows"]:
            profile = getattr(r.user, "profile", None)
            writer.writerow([
                r.name, r.user.email, profile.organisation if profile else "",
                r.modules_completed, r.modules_total,
                "Yes" if r.completed_course else "No",
            ])
        return response

    return _render(
        request,
        "staff/report_compliance.html",
        {
            "active": "admin_reports",
            "report": report,
            "as_at_value": date.isoformat() if date else "",
            "organisations": Organisation.objects.all(),
            "org_id": org.pk if org else "",
        },
    )


@administrator_required
def certificate_register(request):
    """The certificate register: who holds a valid certificate, with codes and
    dates. On-screen, or CSV with ?format=csv."""
    status = request.GET.get("status")
    if status not in ("valid", "revoked"):
        status = None
    certs = services.certificate_register(status=status)

    if request.GET.get("format") == "csv":
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cybaroo-certificate-register.csv"'
        writer = csv.writer(response)
        writer.writerow(["Serial", "Holder", "Email", "Organisation", "Grade",
                         "Issued", "Status", "Revoked"])
        for c in certs:
            profile = getattr(c.user, "profile", None)
            writer.writerow([
                c.serial, c.user.get_full_name() or c.user.email, c.user.email,
                profile.organisation if profile else "", c.grade,
                timezone.localtime(c.issued_at).strftime("%Y-%m-%d"),
                "Revoked" if c.revoked_at else "Valid",
                timezone.localtime(c.revoked_at).strftime("%Y-%m-%d") if c.revoked_at else "",
            ])
        return response

    return _render(
        request,
        "staff/certificates.html",
        {
            "active": "admin_reports",
            "certs": certs,
            "status": status or "",
            "valid_count": sum(1 for c in certs if not c.revoked_at) if not status else None,
        },
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
def org_learners_csv(request, org_id):
    """Download one organisation's learners as CSV — a per-client progress report."""
    org = get_object_or_404(Organisation, pk=org_id)
    rows = services.organisation_members(org)
    rows = services.sort_and_filter(rows)

    response = HttpResponse(content_type="text/csv")
    slug = org.name.lower().replace(" ", "-")
    response["Content-Disposition"] = f'attachment; filename="cybaroo-{slug}-progress.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Name", "Email", "Modules completed", "Modules total", "Overall score",
         "Grade", "Points", "Last active"]
    )
    for r in rows:
        writer.writerow(
            [
                r.name,
                r.user.email,
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
            "organisations": Organisation.objects.all(),
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
def bulk_invite(request):
    """Onboard a whole workplace at once: paste a list of emails or upload a CSV,
    preview exactly what will happen, then create the accounts in one audited
    batch. Each new account is Student (or the chosen role), admin-vouched
    (active + verified), assigned to the chosen organisation, and — least
    privilege — never granted Django staff/superuser. Optionally each is emailed
    a link to set their own password.
    """
    from django.contrib.auth.forms import PasswordResetForm
    from django.utils.crypto import get_random_string

    from authentication.models import UserProfile

    roles = User.Role.choices
    orgs = Organisation.objects.all()

    if request.method != "POST":
        return _render(request, "staff/user_invite.html",
                       {"active": "admin_learners", "roles": roles, "orgs": orgs})

    raw = request.POST.get("emails", "")
    upload = request.FILES.get("csv")
    if upload:
        try:
            raw += "\n" + upload.read().decode("utf-8", "ignore")
        except Exception:
            messages.error(request, "Could not read that file. Paste the emails instead.")

    role = request.POST.get("role") if request.POST.get("role") in User.Role.values else User.Role.STUDENT
    org_id = (request.POST.get("org") or "").strip()
    org = Organisation.objects.filter(pk=org_id).first() if org_id.isdigit() else None
    send_invite = request.POST.get("send_invite") == "on"

    result = services.classify_invites(services.parse_emails(raw))
    ctx = {
        "active": "admin_learners", "roles": roles, "orgs": orgs,
        "result": result, "role": role, "org": org,
        "emails_raw": raw, "send_invite": send_invite,
        "role_label": dict(roles).get(role, role),
    }

    if request.POST.get("action") != "create":
        # Step 1: show the preview.
        return _render(request, "staff/user_invite.html", ctx)

    # Step 2: create the valid, new accounts.
    if not result["new"]:
        messages.error(request, "No new accounts to create.")
        return _render(request, "staff/user_invite.html", ctx)

    created = []
    for email in result["new"]:
        user = User(email=email, role=role, is_active=True, is_verified=True)
        user.set_password(get_random_string(20))  # usable but unknown; they reset it
        user.save()
        UserProfile.objects.create(user=user)
        services.assign_learner_org(user.profile, org)
        created.append(user)
        if send_invite:
            form = PasswordResetForm({"email": email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    email_template_name="authentication/email/password_reset_email.txt",
                    subject_template_name="authentication/email/password_reset_subject.txt",
                )

    where = f" in “{org.name}”" if org else ""
    services.log_action(
        request.user, AdminAction.Kind.BULK_INVITE,
        f"Bulk-invited {len(created)} {dict(roles).get(role, role)} account"
        f"{'' if len(created) == 1 else 's'}{where}",
    )
    messages.success(
        request,
        f"Created {len(created)} account{'' if len(created) == 1 else 's'}"
        f"{' and emailed each a set-password link' if send_invite else ''}.",
    )
    return redirect("staff:learners")


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
def lesson_preview(request, lesson_id):
    """See a lesson exactly as a student would, past the sequential lock and with
    no progress writes. Reuses the real student room renderer."""
    from modules.views import _render_lesson

    lesson = get_object_or_404(Lesson.objects.select_related("module"), pk=lesson_id)
    return _render_lesson(
        request, lesson, preview=True,
        back_url=reverse("staff:lesson_edit", args=[lesson.pk]),
        back_label="Back to editing",
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
