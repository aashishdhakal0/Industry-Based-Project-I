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
from django_ratelimit.decorators import ratelimit

from .forms import LoginCodeForm, LoginForm, RegistrationForm
from .models import UserProfile
from .tokens import make_verification_token, read_verification_token
from .utils import (
    check_login_code,
    hash_login_code,
    make_login_code,
    role_home_url,
    safe_redirect_target,
)

User = get_user_model()

# --------------------------------------------------------------------------
# The half-authenticated window
# --------------------------------------------------------------------------
#
# Between "password was right" and "code was right", the user is NOT logged in.
# Their id sits in the session and login() is called only once the code checks
# out.
#
# The alternative — log them in, then block protected views until the second
# factor passes — leaves a real authenticated session in that window, and
# obliges every view forever after to remember to ask "but did they finish?"
# rather than `is_authenticated`. The first one that forgets is the hole. This
# way a half-finished login is a session key naming a user id: it can't reach
# anything, because it isn't a login.

PENDING_USER_KEY = "pending_2fa_user_id"
PENDING_AT_KEY = "pending_2fa_started_at"
PENDING_NEXT_KEY = "pending_2fa_next"
PENDING_CODE_KEY = "pending_2fa_code_hash"
PENDING_TRIES_KEY = "pending_2fa_attempts"

# An abandoned half-login shouldn't stay valid all day: someone who walks away
# after typing their password has left a loaded gun on a shared machine.
PENDING_MAX_AGE = timedelta(seconds=settings.LOGIN_CODE_TTL_SECONDS)


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


def _start_pending(request, user, next_url, code_hash):
    request.session[PENDING_USER_KEY] = user.pk
    request.session[PENDING_AT_KEY] = timezone.now().isoformat()
    request.session[PENDING_NEXT_KEY] = next_url
    request.session[PENDING_CODE_KEY] = code_hash
    request.session[PENDING_TRIES_KEY] = 0


def _clear_pending(request):
    for key in (
        PENDING_USER_KEY,
        PENDING_AT_KEY,
        PENDING_NEXT_KEY,
        PENDING_CODE_KEY,
        PENDING_TRIES_KEY,
    ):
        request.session.pop(key, None)


def _pending_user(request):
    """The user who passed a password check but hasn't typed the code yet."""
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

    # is_active matters: an account deactivated between the two steps must not
    # be able to finish signing in.
    return User.objects.filter(pk=pk, is_active=True).first()


def _send_login_code(request, user, code):
    body = render_to_string(
        "authentication/email/login_code.txt",
        {
            "first_name": user.first_name,
            "code": code,
            "site_name": settings.SITE_NAME,
            "minutes": settings.LOGIN_CODE_TTL_SECONDS // 60,
        },
    )
    send_mail(
        subject=f"Your {settings.SITE_NAME} sign-in code: {code}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def _complete_login(request, user):
    """Actually sign the user in, and send them where they belong."""
    next_url = request.session.get(PENDING_NEXT_KEY)

    login(request, user)
    # login() cycles the session key but keeps the data, so the pending keys
    # survive into the real session unless we clear them. Read next_url first.
    _clear_pending(request)

    # Showing up counts towards the streak. This replaces the old raw
    # last_active write, which would have fought the streak logic — advancing
    # last_active to today without incrementing the count, so a later lesson the
    # same day would read as "already active today" and never build the streak.
    # record_login goes through the one streak code path. Imported here rather
    # than at module top to keep the auth app free of a modules dependency at
    # import time.
    from modules.gamification import record_login

    record_login(user)

    return redirect(next_url or role_home_url(user))


# The two doors on the login page. Choosing one only sets the heading on the
# form you land on — it is cosmetic framing, NOT a role you get to grant
# yourself. The role that actually decides where you land after signing in is
# read from your account in role_home_url(), never from this. So "log in as
# Administrator" and then typing a Student's credentials signs you in as that
# Student, exactly as it should.
LOGIN_FRAMES = {
    "student": {
        "title": "Student sign-in",
        "lede": "Your lessons, quizzes and progress.",
        "icon": "i-book",
        "accent": "student",
    },
    "admin": {
        "title": "Administrator sign-in",
        "lede": "Manage the platform.",
        "icon": "i-shield",
        "accent": "admin",
    },
}


def _requested_frame(request):
    """The role framing asked for via ?as=, or None for the chooser.

    Validated against the fixed keys, so an unknown or hand-typed value falls
    back to the chooser rather than being trusted. Never influences auth.
    """
    key = request.POST.get("as") or request.GET.get("as")
    return key if key in LOGIN_FRAMES else None


@ratelimit(key="ip", rate="10/h", method="POST", block=False)
def login_view(request):
    """Role chooser, then email + password, then a code we email them.

    The page leads with two institutional "Log in as Student / Administrator"
    buttons (the primary way in). Each opens this same secure form, framed for
    that role. Authentication is unchanged: password, then a code, then a
    session — and the granted role comes from the account, not the button.

    Every account gets the code — see the deviations table in CLAUDE.md. The
    spec asks for an authenticator app; we deviate on the method, not on the
    coverage.

    Rate limiting is task 1.5, folded in here because a login form without one
    is a brute-force target and a sprint is not a reasonable window to leave it
    bare. block=False so we can render a plain-language 429 rather than
    django-ratelimit's bare 403.
    """
    frame_key = _requested_frame(request)
    next_target = safe_redirect_target(request) or ""

    if request.method == "POST":
        if getattr(request, "limited", False):
            return render(request, "authentication/rate_limited.html", status=429)

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            code = make_login_code()
            _start_pending(request, user, next_target, hash_login_code(code))
            _send_login_code(request, user, code)

            return redirect("authentication:login_code")
        # Invalid: fall through and re-render the form, keeping its framing.
    else:
        # A fresh GET with no role picked yet is the chooser — the two big
        # role buttons that are the main way in.
        if frame_key is None:
            return render(
                request,
                "authentication/login_choose.html",
                {"next": next_target, "frames": LOGIN_FRAMES},
            )
        form = LoginForm(request)

    return render(
        request,
        "authentication/login.html",
        {
            "form": form,
            "next": next_target,
            "frame": LOGIN_FRAMES.get(frame_key),
            "frame_key": frame_key or "",
        },
    )


@require_POST
def logout_view(request):
    """POST only — a GET logout can be triggered by any <img> on any site."""
    logout(request)
    return redirect("landing")


@ratelimit(key="ip", rate="10/h", method="POST", block=False)
def login_code(request):
    """The second step: the 6-digit code we just emailed.

    Two independent limits guard this, and both are load-bearing:

      - Per-code attempts (LOGIN_CODE_MAX_ATTEMPTS). Six digits is a million
        combinations, which sounds like plenty until you notice nothing stops
        an attacker who already has the password from simply trying. Five
        wrong guesses and the code dies — they have to start over, which means
        a fresh code lands in the victim's inbox.
      - Per-IP rate limiting, so the "start over" loop isn't free either.

    django-otp used to do the first of these for us via ThrottlingMixin. It's
    gone, so we do it ourselves. This is exactly the sort of thing that quietly
    disappears when a library is swapped out.
    """
    user = _pending_user(request)
    if user is None:
        # No pending login — expired, or someone arrived here directly.
        return redirect("authentication:login")

    if request.method == "POST" and getattr(request, "limited", False):
        return render(request, "authentication/rate_limited.html", status=429)

    form = LoginCodeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        attempts = request.session.get(PENDING_TRIES_KEY, 0) + 1
        request.session[PENDING_TRIES_KEY] = attempts

        if check_login_code(
            form.cleaned_data["code"], request.session.get(PENDING_CODE_KEY)
        ):
            return _complete_login(request, user)

        if attempts >= settings.LOGIN_CODE_MAX_ATTEMPTS:
            _clear_pending(request)
            return render(
                request, "authentication/code_expired.html", status=403
            )

        remaining = settings.LOGIN_CODE_MAX_ATTEMPTS - attempts
        form.add_error(
            "code",
            f"That code didn't match. {remaining} "
            f"{'try' if remaining == 1 else 'tries'} left before we send a new one.",
        )

    return render(
        request,
        "authentication/login_code.html",
        {"form": form, "email": user.email},
    )


@require_POST
def resend_login_code(request):
    """A fresh code, for one that never arrived.

    POST only. As a GET this gets fired by link prefetchers and corporate email
    scanners, silently rotating the user's code out from under them while
    they're still typing it.

    Deliberately does not extend the pending window: issuing a new code resets
    the attempt count, not the clock, so pressing resend forever can't hold a
    half-finished login open indefinitely.
    """
    user = _pending_user(request)
    if user is None:
        return redirect("authentication:login")

    code = make_login_code()
    request.session[PENDING_CODE_KEY] = hash_login_code(code)
    request.session[PENDING_TRIES_KEY] = 0
    _send_login_code(request, user, code)

    return redirect("authentication:login_code")
