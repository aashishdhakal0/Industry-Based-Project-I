"""Student learning URLs, mounted at /learn/."""

from django.urls import path

from quizzes import views as quiz_views

from . import views

app_name = "learn"

urlpatterns = [
    path("", views.browser, name="browser"),
    path("progress/", views.progress, name="progress"),
    path("badges/", views.badges, name="badges"),
    path("certificate/", views.certificate, name="certificate"),
    path("m/<int:order_index>/", views.module_overview, name="module"),
    path(
        "m/<int:order_index>/lesson/<int:lesson_number>/",
        views.lesson,
        name="lesson",
    ),
    path(
        "m/<int:order_index>/lesson/<int:lesson_number>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),
    path(
        "m/<int:order_index>/lesson/<int:lesson_number>/task/",
        views.complete_task,
        name="complete_task",
    ),
    path("m/<int:order_index>/simulation/", views.simulation, name="simulation"),
    path(
        "m/<int:order_index>/simulation/complete/",
        views.complete_simulation,
        name="complete_simulation",
    ),
    # Quiz — module-scoped, but implemented in the quizzes app.
    path("m/<int:order_index>/quiz/", quiz_views.quiz, name="quiz"),
    path("m/<int:order_index>/quiz/save/", quiz_views.save_answer, name="quiz_save"),
    path("m/<int:order_index>/quiz/submit/", quiz_views.submit_quiz, name="quiz_submit"),
    path("m/<int:order_index>/quiz/result/", quiz_views.quiz_result, name="quiz_result"),
    # DEBUG-only content-review preview of every quiz question (404 in production).
    path("m/<int:order_index>/quiz/review/", quiz_views.quiz_review, name="quiz_review"),
]
