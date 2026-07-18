"""Student learning URLs, mounted at /learn/."""

from django.urls import path

from . import views

app_name = "learn"

urlpatterns = [
    path("", views.browser, name="browser"),
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
    path("m/<int:order_index>/simulation/", views.simulation, name="simulation"),
    path(
        "m/<int:order_index>/simulation/complete/",
        views.complete_simulation,
        name="complete_simulation",
    ),
]
