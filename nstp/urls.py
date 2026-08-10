"""Root URL configuration for NSTP."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from modules import views as modules_views

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
    # The student's home — real progress from PostgreSQL (modules.views.dashboard).
    path("dashboard/", modules_views.dashboard, name="dashboard"),
    # The student learning experience — browse, lessons, simulation.
    path("learn/", include("modules.urls")),
    # The Administrator dashboard — the in-platform staff experience. Django's
    # own /admin/ stays available above for raw data management.
    path("manage/", include("staff.urls")),
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
