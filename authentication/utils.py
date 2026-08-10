"""Helpers for the sign-in flow."""

import secrets

from django.conf import settings
from django.urls import reverse
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import url_has_allowed_host_and_scheme


def make_login_code():
    """A fresh numeric code.

    `secrets`, not `random`: random is a Mersenne Twister seeded from the
    clock, and its output is predictable from previous output. That is fine for
    picking a quiz question and catastrophic for the thing standing between an
    attacker and an account.

    Zero-padded, so 42 is "000042" and every code is the same length — a
    variable-length code leaks a little information and looks broken.
    """
    upper = 10 ** settings.LOGIN_CODE_LENGTH
    return str(secrets.randbelow(upper)).zfill(settings.LOGIN_CODE_LENGTH)


def hash_login_code(code):
    """Hash a code for storage.

    The code lives in the session, which is server-side — but "server-side" is
    not "safe to store secrets in plaintext". Sessions get dumped in debugging,
    copied into fixtures, and read by anyone with database access. Hash it.

    salted_hmac keys off SECRET_KEY, so a code hashed by one deployment means
    nothing to another. It is deliberately fast: this is a 6-digit number with
    a 10-minute life and a 5-attempt cap, not a password, and a slow hash here
    would only make our own login slow.
    """
    return salted_hmac("cybaroo.login-code", code).hexdigest()


def check_login_code(code, expected_hash):
    """Compare a submitted code against the stored hash, in constant time.

    constant_time_compare, not ==: string comparison returns as soon as it
    finds a difference, so how long it takes reveals how much of the code was
    right. That is a real attack on a 6-digit secret, and the fix costs nothing.
    """
    return constant_time_compare(hash_login_code(code), expected_hash or "")


def role_home_url(user):
    """Where this user belongs after signing in.

    One helper rather than a redirect scattered through the views, so "where
    does an Instructor land" has exactly one answer.
    """
    User = user.__class__
    if user.role == User.Role.ADMINISTRATOR:
        # The in-platform Administrator dashboard, not Django's raw /admin/.
        # /admin/ is still reachable directly (and linked from the sidebar) for
        # raw data management, but the polished oversight surface is home.
        return reverse("staff:overview")
    # Instructors land on the dashboard for now; their CMS arrives in Sprint 2.
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
