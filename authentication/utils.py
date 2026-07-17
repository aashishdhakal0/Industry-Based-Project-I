"""Helpers for the sign-in flow."""

import base64
from io import BytesIO

import qrcode
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django_otp.plugins.otp_totp.models import TOTPDevice


def confirmed_totp_device(user):
    """The user's usable TOTP device, or None.

    `confirmed=True` is the whole point: an unconfirmed device is one that was
    generated but never proven — the user may never have scanned it. Treating
    it as a second factor would mean anyone who reached the setup page had
    "2FA" without ever holding the phone.
    """
    return TOTPDevice.objects.filter(user=user, confirmed=True).first()


def pending_totp_device(user):
    """The user's half-finished device, or None."""
    return TOTPDevice.objects.filter(user=user, confirmed=False).first()


def totp_qr_data_uri(device):
    """Render the device's provisioning URI as an inline PNG data URI.

    django-otp renders a QR automatically **only inside the admin**, so the
    user-facing flow has to build its own from `config_url`.

    Inline data URI rather than a view serving PNG bytes: our CSP allows
    `img-src 'self' data:`, so it renders — and more importantly a URL that
    returns the QR is a URL that hands out the TOTP secret to anyone who can
    guess it. The secret should never have an address.
    """
    image = qrcode.make(device.config_url)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def totp_manual_key(device):
    """The base32 secret, for someone who can't scan the QR.

    `device.key` is hex; authenticator apps want base32. Offering this matters
    for accessibility — a screen-reader user cannot scan a QR code, and without
    a typeable key 2FA would simply be closed to them.
    """
    return base64.b32encode(device.bin_key).decode("ascii")


def role_home_url(user):
    """Where this user belongs after signing in.

    One helper rather than a redirect scattered through the views, so "where
    does an Instructor land" has exactly one answer.
    """
    User = user.__class__
    if user.role == User.Role.ADMINISTRATOR and user.is_staff:
        return reverse("admin:index")
    # Instructors land on the dashboard for now; their CMS arrives in Sprint 2.
    # An Administrator without is_staff would be bounced by the admin's own
    # login, so they come here too rather than into a dead end.
    return reverse("dashboard")


def safe_redirect_target(request):
    """The validated ?next= target, or None.

    `url_has_allowed_host_and_scheme` is the open-redirect guard: without it,
    /login/?next=https://evil.example would hand an attacker a login page on
    our domain that forwards to theirs — a phishing kit, hosted by us, on a
    cyber-security training platform.
    """
    target = request.POST.get("next") or request.GET.get("next")
    if target and url_has_allowed_host_and_scheme(
        url=target,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return target
    return None
