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
    path("activity/", views.activity, name="activity"),
    path("users/new/", views.user_new, name="user_new"),
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
