"""Privileged user-management actions, each its own POST endpoint.

Every one is administrator-only, POST + CSRF, re-checks the target server-side,
logs to the audit trail, and enforces two lockout guardrails that matter on a
security platform:

  - an admin cannot change their own role or deactivate themselves, and
  - the last remaining active Administrator cannot be demoted or deactivated.

Between them, there is no sequence of clicks that leaves the platform with no
one able to administer it.
"""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from authentication.decorators import administrator_required
from authentication.models import User

from . import services
from .models import AdminAction


def _other_active_admin_exists(exclude_id):
    return (
        User.objects.filter(role=User.Role.ADMINISTRATOR, is_active=True)
        .exclude(pk=exclude_id)
        .exists()
    )


def _is_last_active_admin(user):
    return (
        user.role == User.Role.ADMINISTRATOR
        and user.is_active
        and not _other_active_admin_exists(user.pk)
    )


def _back(user):
    return redirect(reverse("staff:learner_detail", args=[user.pk]))


@administrator_required
@require_POST
def change_role(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    new_role = request.POST.get("role")

    if new_role not in User.Role.values:
        raise PermissionDenied("Unknown role.")

    if target.pk == request.user.pk:
        messages.error(request, "You can't change your own role.")
        return _back(target)

    if new_role != User.Role.ADMINISTRATOR and _is_last_active_admin(target):
        messages.error(
            request, "This is the last active Administrator — promote someone else first."
        )
        return _back(target)

    if target.role == new_role:
        messages.info(request, f"{target.email} is already {target.get_role_display()}.")
        return _back(target)

    old = target.get_role_display()
    target.role = new_role
    target.save(update_fields=["role"])

    services.log_action(
        request.user,
        AdminAction.Kind.ROLE_CHANGE,
        f"Changed {target.email} from {old} to {target.get_role_display()}",
        target_user=target,
    )
    messages.success(request, f"{target.email} is now {target.get_role_display()}.")
    return _back(target)


@administrator_required
@require_POST
def toggle_active(request, user_id):
    target = get_object_or_404(User, pk=user_id)

    if target.pk == request.user.pk:
        messages.error(request, "You can't deactivate your own account.")
        return _back(target)

    if target.is_active and _is_last_active_admin(target):
        messages.error(
            request, "This is the last active Administrator — you can't deactivate them."
        )
        return _back(target)

    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])

    kind = AdminAction.Kind.ACTIVATE if target.is_active else AdminAction.Kind.DEACTIVATE
    verb = "Activated" if target.is_active else "Deactivated"
    services.log_action(
        request.user, kind, f"{verb} {target.email}", target_user=target
    )
    messages.success(request, f"{verb} {target.email}.")
    return _back(target)


@administrator_required
@require_POST
def resend_verification(request, user_id):
    target = get_object_or_404(User, pk=user_id)

    # Imported here to keep the auth app free of a staff dependency at import.
    from authentication.views import _send_verification_email

    _send_verification_email(request, target)
    services.log_action(
        request.user,
        AdminAction.Kind.RESEND_VERIFICATION,
        f"Resent verification to {target.email}",
        target_user=target,
    )
    messages.success(request, f"Verification email sent to {target.email}.")
    return _back(target)


@administrator_required
@require_POST
def nudge(request, user_id):
    target = get_object_or_404(User, pk=user_id)

    login_url = request.build_absolute_uri(reverse("authentication:login"))
    body = (
        f"Hi {target.first_name or 'there'},\n\n"
        f"Just a friendly nudge from {settings.SITE_NAME}: your cyber-safety "
        "training is waiting whenever you're ready. Picking up where you left "
        "off only takes a few minutes.\n\n"
        f"Sign in here: {login_url}\n\n"
        "See you in there."
    )
    send_mail(
        subject=f"A quick nudge from {settings.SITE_NAME}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[target.email],
    )
    services.log_action(
        request.user,
        AdminAction.Kind.NUDGE,
        f"Sent a nudge to {target.email}",
        target_user=target,
    )
    messages.success(request, f"Nudge sent to {target.email}.")
    return _back(target)


@administrator_required
@require_POST
def toggle_flag(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    profile = services.g.get_profile(target)

    profile.flagged = not profile.flagged
    profile.flag_reason = request.POST.get("reason", "").strip() if profile.flagged else ""
    profile.save(update_fields=["flagged", "flag_reason"])

    kind = AdminAction.Kind.FLAG if profile.flagged else AdminAction.Kind.UNFLAG
    verb = "Flagged" if profile.flagged else "Cleared the flag on"
    services.log_action(
        request.user, kind, f"{verb} {target.email}", target_user=target
    )
    messages.success(request, f"{verb} {target.email}.")
    return _back(target)
