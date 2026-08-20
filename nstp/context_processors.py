"""Template context shared by every page."""

from django.conf import settings


def site(request):
    """Expose the platform's name as {{ site_name }}.

    Templates must never spell the name out literally — read it from here, so
    rebranding is one edit to SITE_NAME in settings.
    """
    return {"site_name": settings.SITE_NAME}


def student_nav(request):
    """Profile summary for the top-right chip, on every student page.

    Kept small and query-cheap (one profile fetch; level/tier are pure functions
    of its cached points). Students only — administrators use the console chrome,
    and anonymous/auth pages get nothing.
    """
    user = getattr(request, "user", None)
    if not (user and user.is_authenticated) or user.is_administrator:
        return {}

    from modules import gamification as g

    profile = g.get_profile(user)
    initial = (user.first_name or user.email or "?")[:1].upper()
    name = user.get_full_name() or user.first_name or user.email
    return {
        "nav_profile": {
            "initial": initial,
            "name": name,
            "tier": g.tier_for_points(profile.points),
            "level": g.level_for_points(profile.points),
        }
    }
