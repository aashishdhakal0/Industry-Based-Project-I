"""Administrator dashboard URLs, mounted at /manage/."""

from django.urls import path

from . import useractions, views

app_name = "staff"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("learners/", views.learners, name="learners"),
    path("learners/export.csv", views.learners_csv, name="learners_csv"),
    path("learners/<int:user_id>/", views.learner_detail, name="learner_detail"),
    path("organisations/", views.organisations, name="organisations"),
    path("organisations/new/", views.org_new, name="org_new"),
    path("organisations/none/", views.unassigned, name="unassigned"),
    path("organisations/<int:org_id>/", views.org_detail, name="org_detail"),
    path("organisations/<int:org_id>/export.csv", views.org_learners_csv, name="org_learners_csv"),
    path("organisations/<int:org_id>/delete/", useractions.org_delete, name="org_delete"),
    path("organisations/<int:org_id>/note/", useractions.send_note_org, name="send_note_org"),
    path("activity/", views.activity, name="activity"),
    path("activity/export.csv", views.activity_csv, name="activity_csv"),
    # Reporting & compliance hub.
    path("reports/", views.reports, name="reports"),
    path("reports/compliance/", views.report_compliance, name="report_compliance"),
    path("reports/certificates/", views.certificate_register, name="certificate_register"),
    path("certificates/<int:cert_id>/revoke/", useractions.revoke_cert, name="revoke_cert"),
    path("theme/", views.set_theme, name="set_theme"),
    path("users/new/", views.user_new, name="user_new"),
    path("users/invite/", views.bulk_invite, name="bulk_invite"),
    # User-management actions (POST only, admin only, audit-logged).
    path("users/<int:user_id>/role/", useractions.change_role, name="change_role"),
    path("users/<int:user_id>/active/", useractions.toggle_active, name="toggle_active"),
    path(
        "users/<int:user_id>/resend-verification/",
        useractions.resend_verification,
        name="resend_verification",
    ),
    path("users/<int:user_id>/nudge/", useractions.nudge, name="nudge"),
    path("users/<int:user_id>/flag/", useractions.toggle_flag, name="toggle_flag"),
    path("users/<int:user_id>/organisation/", useractions.assign_org, name="assign_org"),
    path("users/<int:user_id>/note/", useractions.send_note_user, name="send_note_user"),
    path("users/<int:user_id>/private-note/", useractions.add_note, name="add_note"),
    path("users/<int:user_id>/reset/", useractions.reset, name="reset"),
    path("users/<int:user_id>/password-reset/", useractions.send_password_reset, name="send_password_reset"),
    # Bulk actions over a selection from the learners table.
    path("learners/bulk/", useractions.bulk_action, name="bulk_action"),
    # Content management: list, publish, and drill in to edit.
    path("content/", views.content, name="content"),
    path(
        "content/m/<int:order_index>/publish/",
        views.content_publish,
        name="content_publish",
    ),
    path("content/m/<int:order_index>/", views.module_detail, name="module_detail"),
    path("content/m/<int:order_index>/quiz/", views.quiz_view, name="quiz_view"),
    path("content/lesson/<int:lesson_id>/edit/", views.lesson_edit, name="lesson_edit"),
    path("content/lesson/<int:lesson_id>/preview/", views.lesson_preview, name="lesson_preview"),
    path(
        "content/lesson/<int:lesson_id>/publish/",
        views.lesson_publish,
        name="lesson_publish",
    ),
    path(
        "content/question/<int:question_id>/edit/",
        views.question_edit,
        name="question_edit",
    ),
]
