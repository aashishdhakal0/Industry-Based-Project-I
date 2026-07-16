"""Root URL configuration for NSTP."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
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
