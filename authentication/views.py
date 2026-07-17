"""Registration, email verification, sign-in and two-factor authentication."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_ratelimit.decorators import ratelimit

from .forms import LoginForm, RegistrationForm, TOTPTokenForm
from .models import UserProfile
from .tokens import make_verification_token, read_verification_token
from .utils import (
    confirmed_totp_device,
    pending_totp_device,
    role_home_url,
    safe_redirect_target,
    totp_manual_key,
    totp_qr_data_uri,
)

User = get_user_model()

# --------------------------------------------------------------------------
# The half-authenticated window
# --------------------------------------------------------------------------
#
# Between "password was right" and "second factor was right", the user is NOT
# logged in. We hold their id in the session and call login() only once the
# code checks out.
#
# The alternative — log them in, then block protected views until OTP passes —
# is what django-otp's own examples do, and it means a real authenticated
# session exists in that window. Every view then has to remember to ask
# `is_verified()` rather than `is_authenticated`, and the first one that
# forgets is a hole. This way a half-finished login is just a session key
# naming a user id: it can't reach anything, because it isn't a login.

PENDING_USER_KEY = "pending_2fa_user_id"
PENDING_AT_KEY = "pending_2fa_started_at"
PENDING_NEXT_KEY = "pending_2fa_next"

# An abandoned half-login shouldn't stay valid all day: someone who walks away
# after typing their password has left a loaded gun on a shared machine.
PENDING_MAX_AGE = timedelta(minutes=10)


def _send_verification_email(request, user):
    """Post the signed link to the address the user gave us."""
    verify_url = request.build_absolute_uri(
        reverse("authentication:verify", args=[make_verification_token(user)])
    )
    # render_to_string doesn't run context processors without a request, so
    # site_name is passed explicitly rather than relying on {{ site_name }}
    # silently rendering empty.
    body = render_to_string(
        "authentication/email/verify_email.txt",
        {
            "first_name": user.first_name,
            "verify_url": verify_url,
            "site_name": settings.SITE_NAME,
        },
    )
    send_mail(
        subject=f"Confirm your email — {settings.SITE_NAME}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # User and profile are one unit: a user without a profile would
            # break every dashboard query downstream.
            with transaction.atomic():
                user = form.save()
                UserProfile.objects.create(
                    user=user,
                    organisation=form.cleaned_data.get("organisation", ""),
                )

            _send_verification_email(request, user)

            # The address goes in the session, not the URL: it is only needed to
            # render "we sent it to <you>", and a querystring would put it in
            # browser history and server logs.
            request.session["pending_verification_email"] = user.email
            return redirect("authentication:check_inbox")
    else:
        form = RegistrationForm()

    return render(request, "authentication/register.html", {"form": form})


def check_inbox(request):
    return render(
        request,
        "authentication/check_inbox.html",
        {"email": request.session.get("pending_verification_email")},
    )


def verify(request, token):
    """Open the emailed link.

    Idempotent by design: the token stays valid until it expires, so a second
    click must not look like a failure. An already-verified user is simply told
    they're good to go.
    """
    try:
        uid = read_verification_token(token)
    except signing.SignatureExpired:
        return render(request, "authentication/link_expired.html", status=410)
    except signing.BadSignature:
        return render(request, "authentication/link_invalid.html", status=400)

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        # Correctly signed, but the account is gone — treat as a dead link.
        return render(request, "authentication/link_invalid.html", status=400)

    if not user.is_verified:
        user.is_verified = True
        user.is_active = True
        user.save(update_fields=["is_verified", "is_active"])

    request.session.pop("pending_verification_email", None)
    return render(request, "authentication/verified.html")


# --------------------------------------------------------------------------
# Sign in
# --------------------------------------------------------------------------


def _start_pending(request, user, next_url=None):
    request.session[PENDING_USER_KEY] = user.pk
    request.session[PENDING_AT_KEY] = timezone.now().isoformat()
    request.session[PENDING_NEXT_KEY] = next_url


def _clear_pending(request):
    for key in (PENDING_USER_KEY, PENDING_AT_KEY, PENDING_NEXT_KEY):
        request.session.pop(key, None)


def _pending_user(request):
    """The user who passed a password check but hasn't finished 2FA."""
    pk = request.session.get(PENDING_USER_KEY)
    started_at = request.session.get(PENDING_AT_KEY)
    if not pk or not started_at:
        return None

    try:
        started = timezone.datetime.fromisoformat(started_at)
    except ValueError:
        _clear_pending(request)
        return None

    if timezone.now() - started > PENDING_MAX_AGE:
        _clear_pending(request)
        return None

    # is_active filter matters: an account deactivated between the two steps
    # must not be able to finish signing in.
    return User.objects.filter(pk=pk, is_active=True).first()


def _complete_login(request, user, device=None):
    """Actually sign the user in, and send them where they belong."""
    login(request, user)
    if device is not None:
        # Records *which* device satisfied the second factor, so
        # request.user.is_verified() is true for the rest of the session.
        otp_login(request, device)

    next_url = request.session.get(PENDING_NEXT_KEY)
    _clear_pending(request)

    # Touched on every sign-in; Sprint 4 builds the streak on top of it.
    UserProfile.objects.filter(user=user).update(last_active=timezone.now())

    return redirect(next_url or role_home_url(user))


@ratelimit(key="ip", rate="10/h", method="POST", block=False)
def login_view(request):
    """Email + password, then a second factor if this account has one.

    Rate limiting is task 1.5, folded in here because a login form without one
    is a brute-force target, and shipping it bare for a sprint is not a
    reasonable window. block=False so we can render a plain-language 429 rather
    than django-ratelimit's bare 403.
    """
    if request.method == "POST" and getattr(request, "limited", False):
        return render(request, "authentication/rate_limited.html", status=429)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            next_url = safe_redirect_target(request)
            device = confirmed_totp_device(user)

            if device is not None:
                # Has 2FA — Student or otherwise. Ask for the code.
                _start_pending(request, user, next_url)
                return redirect("authentication:two_factor_verify")

            if user.requires_2fa:
                # Instructor/Administrator with no device: setup is the wall,
                # not a suggestion. They are not logged in until it's done.
                _start_pending(request, user, next_url)
                return redirect("authentication:two_factor_setup")

            # Student without 2FA: straight in. See User.requires_2fa for why.
            return _complete_login(request, user)
    else:
        form = LoginForm(request)

    return render(
        request,
        "authentication/login.html",
        {"form": form, "next": safe_redirect_target(request) or ""},
    )


@require_POST
def logout_view(request):
    """POST only — a GET logout can be triggered by any <img> on any site."""
    logout(request)
    return redirect("landing")


# --------------------------------------------------------------------------
# Two-factor
# --------------------------------------------------------------------------


def two_factor_setup(request):
    """Enrol an authenticator app.

    Reachable two ways, on purpose:
      - mid-login, by an Instructor/Administrator who must enrol (pending
        session, not yet logged in), and
      - by an already-signed-in Student choosing to turn it on.

    That second path is what makes "optional but encouraged" a real offer
    rather than a line in a report.
    """
    user = _pending_user(request)
    mid_login = user is not None
    if user is None and request.user.is_authenticated:
        user = request.user

    if user is None:
        return redirect("authentication:login")

    if confirmed_totp_device(user) is not None:
        # Already set up. Nothing to do here.
        if mid_login:
            return redirect("authentication:two_factor_verify")
        return redirect(role_home_url(user))

    device = pending_totp_device(user)
    if device is None:
        device = TOTPDevice.objects.create(user=user, name="default", confirmed=False)

    form = TOTPTokenForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if device.verify_token(form.cleaned_data["token"]):
            # Confirmed only once they've proved they hold the phone. Until
            # this line the device is a secret we generated and nobody scanned.
            device.confirmed = True
            device.save(update_fields=["confirmed"])

            if mid_login:
                return _complete_login(request, user, device)

            otp_login(request, device)
            return redirect(role_home_url(user))

        form.add_error(
            "token",
            "That code didn't match. Check your app and try the current code — "
            "they change every 30 seconds.",
        )

    return render(
        request,
        "authentication/two_factor_setup.html",
        {
            "form": form,
            "qr_data_uri": totp_qr_data_uri(device),
            "manual_key": totp_manual_key(device),
            "required": user.requires_2fa,
            "mid_login": mid_login,
        },
    )


@ratelimit(key="ip", rate="10/h", method="POST", block=False)
def two_factor_verify(request):
    """The code prompt on subsequent sign-ins.

    TOTPDevice carries django-otp's ThrottlingMixin, so repeated wrong codes
    back off per-device on their own. The IP limit here is a second layer: the
    device throttle protects one account, this protects the form.
    """
    user = _pending_user(request)
    if user is None:
        # No pending login — expired, or someone arrived here directly.
        return redirect("authentication:login")

    device = confirmed_totp_device(user)
    if device is None:
        return redirect("authentication:two_factor_setup")

    if request.method == "POST" and getattr(request, "limited", False):
        return render(request, "authentication/rate_limited.html", status=429)

    form = TOTPTokenForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if device.verify_token(form.cleaned_data["token"]):
            return _complete_login(request, user, device)
        form.add_error(
            "token",
            "That code didn't match. Codes change every 30 seconds — try the "
            "one showing now.",
        )

    return render(request, "authentication/two_factor_verify.html", {"form": form})
