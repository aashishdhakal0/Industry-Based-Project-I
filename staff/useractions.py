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
from authentication.models import Organisation, User

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


@administrator_required
@require_POST
def assign_org(request, user_id):
    """Assign a learner to an organisation, reassign, or clear it (empty value).

    Writes through the service helper so the FK and the text mirror stay in step.
    Redirects back to the org page when the action came from there, otherwise to
    the learner's profile.
    """
    target = get_object_or_404(User, pk=user_id)
    profile = services.g.get_profile(target)

    org_id = (request.POST.get("org") or "").strip()
    org = get_object_or_404(Organisation, pk=org_id) if org_id else None
    services.assign_learner_org(profile, org)

    if org:
        summary = f"Assigned {target.email} to “{org.name}”"
    else:
        summary = f"Removed {target.email} from their organisation"
    services.log_action(
        request.user, AdminAction.Kind.ASSIGN_ORG, summary, target_user=target
    )
    messages.success(request, summary + ".")

    from_org = (request.POST.get("from_org") or "").strip()
    if from_org:
        return redirect(reverse("staff:org_detail", args=[from_org]))
    return _back(target)


def _email_note(recipients, message, from_admin):
    """Send a plain note from an administrator to one or more members."""
    body = (
        f"{message}\n\n—\nThis note was sent by a {settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'Cybaroo'} "
        f"administrator ({from_admin.get_full_name() or from_admin.email})."
    )
    sent = 0
    for email in recipients:
        if not email:
            continue
        send_mail(
            subject="A note from your Cybaroo administrator",
            message=body,
            from_email=None,               # DEFAULT_FROM_EMAIL
            recipient_list=[email],
            fail_silently=False,
        )
        sent += 1
    return sent


@administrator_required
@require_POST
def org_delete(request, org_id):
    """Delete an organisation. Its members are detached (they become unassigned),
    never deleted — people outlive the group. Audited."""
    org = get_object_or_404(Organisation, pk=org_id)
    name = org.name
    # Detach members cleanly: clear the FK AND the text mirror so nobody is left
    # pointing at a group that no longer exists.
    for profile in org.members.all():
        services.assign_learner_org(profile, None)
    org.delete()
    services.log_action(request.user, AdminAction.Kind.DELETE_ORG, f"Deleted organisation “{name}”")
    messages.success(request, f"Deleted “{name}”. Its members are now unassigned.")
    return redirect(reverse("staff:organisations"))


@administrator_required
@require_POST
def send_note_org(request, org_id):
    """Email a note to every member of an organisation. Audited."""
    org = get_object_or_404(Organisation, pk=org_id)
    message = (request.POST.get("message") or "").strip()
    if not message:
        messages.error(request, "Write a note before sending.")
        return redirect(reverse("staff:org_detail", args=[org.pk]))

    emails = list(org.members.values_list("user__email", flat=True))
    sent = _email_note(emails, message, request.user)
    services.log_action(
        request.user, AdminAction.Kind.NOTE_ORG,
        f"Sent a note to “{org.name}” ({sent} member{'' if sent == 1 else 's'})",
    )
    messages.success(request, f"Sent your note to {sent} member{'' if sent == 1 else 's'} of “{org.name}”.")
    return redirect(reverse("staff:org_detail", args=[org.pk]))


@administrator_required
@require_POST
def send_note_user(request, user_id):
    """Email a note to a single learner. Audited."""
    target = get_object_or_404(User, pk=user_id)
    message = (request.POST.get("message") or "").strip()
    if not message:
        messages.error(request, "Write a note before sending.")
        return _back(target)

    _email_note([target.email], message, request.user)
    services.log_action(
        request.user, AdminAction.Kind.NOTE_USER,
        f"Sent a note to {target.email}", target_user=target,
    )
    messages.success(request, f"Sent your note to {target.email}.")
    return _back(target)
