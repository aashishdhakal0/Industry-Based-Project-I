"""Root URL configuration for NSTP."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # The public homepage. Declared before the authentication include: path("")
    # only matches an empty remainder, so /register/ still falls through.
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    # The student's home. Placeholder data for now (Sprint 4 wires it to real
    # ProgressRecord/QuizResult aggregates), but gated from day one — an
    # unprotected dashboard tends to stay unprotected, and CLAUDE.md requires
    # every view to carry its own auth check.
    path(
        "dashboard/",
        login_required(TemplateView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),
    path("", include("authentication.urls")),
]

if settings.DEBUG:
    # The component library. Development only — it is not a product page, and
    # gating it here means it cannot be reached in production even by URL.
    urlpatterns += [
        path(
            "styleguide/",
            TemplateView.as_view(template_name="styleguide.html"),
            name="styleguide",
        ),
    ]
