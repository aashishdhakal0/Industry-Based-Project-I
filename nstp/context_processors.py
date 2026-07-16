"""Template context shared by every page."""

from django.conf import settings


def site(request):
    """Expose the platform's name as {{ site_name }}.

    Templates must never spell the name out literally — read it from here, so
    rebranding is one edit to SITE_NAME in settings.
    """
    return {"site_name": settings.SITE_NAME}
