"""Registration and email verification."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import RegistrationForm
from .models import UserProfile
from .tokens import make_verification_token, read_verification_token

User = get_user_model()


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
