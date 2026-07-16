"""Root URL configuration for NSTP."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from .placeholder_content import MODULES, THREAT_STATS

# Placeholder context for the pages that show the six modules. Sprint 2 replaces
# MODULES with real Module rows and this goes away; until then it keeps the six
# names in one place instead of four templates that would drift apart.
_module_context = {"modules": MODULES}

urlpatterns = [
    path("admin/", admin.site.urls),
    # The public homepage. Declared before the authentication include: path("")
    # only matches an empty remainder, so /register/ still falls through.
    path(
        "",
        TemplateView.as_view(
            template_name="landing.html",
            extra_context={**_module_context, "threat_stats": THREAT_STATS},
        ),
        name="landing",
    ),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path(
        "modules/",
        TemplateView.as_view(
            template_name="modules.html", extra_context=_module_context
        ),
        name="modules",
    ),
    # The student's home. Placeholder data for now (Sprint 4 wires it to real
    # ProgressRecord/QuizResult aggregates), but gated from day one — an
    # unprotected dashboard tends to stay unprotected, and CLAUDE.md requires
    # every view to carry its own auth check.
    path(
        "dashboard/",
        login_required(
            TemplateView.as_view(
                template_name="dashboard.html", extra_context=_module_context
            )
        ),
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
            TemplateView.as_view(
                template_name="styleguide.html", extra_context=_module_context
            ),
            name="styleguide",
        ),
    ]
