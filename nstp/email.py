"""HTTPS email backend for Resend.

Some free hosts (Render's free tier) block outbound SMTP (port 587), so an SMTP
send hangs at socket.connect until the Gunicorn worker times out and dies,
500-ing the request. This backend sends over Resend's HTTPS API
(https://api.resend.com/emails, port 443) instead, which those hosts allow.

It is a drop-in Django email backend, so every existing send in the app works
unchanged: the 6-digit 2FA login codes, registration verification links,
password-reset emails and admin nudges all flow through here once EMAIL_BACKEND
points at it. Local development keeps the console backend and never touches this.

Robustness (so a provider outage never kills a worker or 500s the site):
  - every request has a hard timeout (EMAIL_API_TIMEOUT, default 10s), well
    inside Gunicorn's 30s worker timeout, so it can never hang the way SMTP did;
  - when EMAIL_FAIL_SILENTLY is true (set it in production), a failure is logged
    and swallowed instead of raised, so email trouble never becomes a 500.

Uses only the standard library — no extra dependency to install or break.
"""

import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger("nstp.email")

RESEND_ENDPOINT = "https://api.resend.com/emails"


class ResendEmailBackend(BaseEmailBackend):
    """Send Django EmailMessages via Resend's HTTPS API."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        # A global switch (EMAIL_FAIL_SILENTLY) can force silent failures even
        # when a caller passed fail_silently=False, so no email path can 500 the
        # site in production. Per-call fail_silently still wins when it is True.
        self.fail_silently = fail_silently or getattr(
            settings, "EMAIL_FAIL_SILENTLY", False
        )
        self.api_key = getattr(settings, "RESEND_API_KEY", "")
        self.timeout = getattr(settings, "EMAIL_API_TIMEOUT", 10)

    def send_messages(self, email_messages):
        """Send one or more messages; return the count actually accepted."""
        if not email_messages:
            return 0
        if not self.api_key:
            logger.error("RESEND_API_KEY is not set; cannot send email over the API.")
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY is not configured.")
            return 0

        sent = 0
        for message in email_messages:
            if self._send_one(message):
                sent += 1
        return sent

    def _payload(self, message):
        payload = {
            "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
            "to": list(message.to),
            "subject": message.subject,
            "text": message.body,
        }
        if message.cc:
            payload["cc"] = list(message.cc)
        if message.bcc:
            payload["bcc"] = list(message.bcc)
        if message.reply_to:
            payload["reply_to"] = list(message.reply_to)
        # Carry an HTML alternative if the message has one (EmailMultiAlternatives).
        for content, mimetype in getattr(message, "alternatives", None) or []:
            if mimetype == "text/html":
                payload["html"] = content
        return payload

    def _send_one(self, message):
        payload = self._payload(message)
        if not payload["to"]:
            return False

        request = urllib.request.Request(
            RESEND_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response.read()
            return True
        except urllib.error.HTTPError as exc:
            # 401 = bad key, 403/422 = unverified sender domain, etc. Log the body
            # so the exact reason is visible in the Render logs.
            body = exc.read().decode("utf-8", "ignore")[:500]
            logger.error("Resend API error %s: %s", exc.code, body)
            if not self.fail_silently:
                raise
            return False
        except Exception as exc:  # timeout, DNS, connection reset, ...
            logger.error("Resend email send failed: %s", exc)
            if not self.fail_silently:
                raise
            return False
