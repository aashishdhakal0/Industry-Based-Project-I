"""Role gates for views.

An enforced control, not a hidden link: a non-administrator who types the URL
gets a real 403, exactly as the sequential module lock does (CLAUDE.md). Hiding
the sidebar item is presentation; this is the control.
"""

from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .models import User


def administrator_required(view):
    """Only signed-in Administrators may proceed.

    Anonymous users are sent to log in (with ?next= back here); a signed-in
    non-administrator is denied outright with a 403 rather than bounced to
    login, because logging in as themselves again would not help.
    """

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if request.user.role != User.Role.ADMINISTRATOR:
            raise PermissionDenied("Administrators only.")
        return view(request, *args, **kwargs)

    return wrapped
