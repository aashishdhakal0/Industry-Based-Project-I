"""The Resend HTTPS email backend (nstp.email.ResendEmailBackend).

Proves the swap-in works for the whole app (send_mail routes through it), that
an HTML alternative is carried, and — the point of the change — that a provider
failure is bounded by a timeout and never raises when EMAIL_FAIL_SILENTLY is on,
so it can't 500 the site or hang a worker.
"""

import json
import urllib.error

import pytest
from django.core.mail import EmailMultiAlternatives, send_mail

BACKEND = "nstp.email.ResendEmailBackend"


class _FakeResp:
    def __init__(self, body=b'{"id": "email_123"}'):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


@pytest.fixture
def use_resend(settings):
    settings.EMAIL_BACKEND = BACKEND
    settings.RESEND_API_KEY = "re_test_key"
    settings.EMAIL_API_TIMEOUT = 7
    settings.EMAIL_FAIL_SILENTLY = False
    return settings


def _capture(monkeypatch):
    grabbed = {}

    def fake_urlopen(request, timeout=None):
        grabbed["url"] = request.full_url
        grabbed["auth"] = request.get_header("Authorization")
        grabbed["user_agent"] = request.get_header("User-agent")
        grabbed["timeout"] = timeout
        grabbed["body"] = json.loads(request.data.decode("utf-8"))
        return _FakeResp()

    monkeypatch.setattr("nstp.email.urllib.request.urlopen", fake_urlopen)
    return grabbed


def test_send_mail_posts_to_the_resend_api(use_resend, monkeypatch):
    grabbed = _capture(monkeypatch)
    n = send_mail("Your Cybaroo code", "123456", "noreply@x.com", ["user@x.com"])
    assert n == 1
    assert grabbed["url"] == "https://api.resend.com/emails"
    assert grabbed["auth"] == "Bearer re_test_key"
    assert grabbed["timeout"] == 7                       # the hard timeout is applied
    assert grabbed["body"]["to"] == ["user@x.com"]
    assert grabbed["body"]["subject"] == "Your Cybaroo code"
    assert grabbed["body"]["text"] == "123456"
    assert grabbed["body"]["from"] == "noreply@x.com"


def test_request_sets_an_explicit_user_agent(use_resend, monkeypatch):
    # Resend/Cloudflare 403s (code 1010) without a User-Agent, or with the
    # default urllib one. Assert we send an explicit product User-Agent.
    from nstp.email import USER_AGENT

    grabbed = _capture(monkeypatch)
    send_mail("s", "b", "noreply@x.com", ["user@x.com"])
    assert grabbed["user_agent"] == USER_AGENT
    assert grabbed["user_agent"]                       # never empty
    assert "urllib" not in (grabbed["user_agent"] or "").lower()


def test_html_alternative_is_carried(use_resend, monkeypatch):
    grabbed = _capture(monkeypatch)
    msg = EmailMultiAlternatives("Hi", "plain text", "noreply@x.com", ["user@x.com"])
    msg.attach_alternative("<b>rich</b>", "text/html")
    assert msg.send() == 1
    assert grabbed["body"]["text"] == "plain text"
    assert grabbed["body"]["html"] == "<b>rich</b>"


def test_failure_is_swallowed_when_fail_silently_is_on(use_resend, monkeypatch):
    # This is the production setting: an outage must not raise (no 500, no worker
    # death), even though the caller used the default fail_silently=False.
    use_resend.EMAIL_FAIL_SILENTLY = True

    def boom(request, timeout=None):
        raise urllib.error.URLError("connection reset")

    monkeypatch.setattr("nstp.email.urllib.request.urlopen", boom)
    n = send_mail("s", "b", "noreply@x.com", ["user@x.com"])   # must NOT raise
    assert n == 0


def test_failure_raises_when_not_silent(use_resend, monkeypatch):
    def boom(request, timeout=None):
        raise urllib.error.URLError("connection reset")

    monkeypatch.setattr("nstp.email.urllib.request.urlopen", boom)
    with pytest.raises(urllib.error.URLError):
        send_mail("s", "b", "noreply@x.com", ["user@x.com"])


def test_http_error_is_logged_and_reraised(use_resend, monkeypatch):
    def http_error(request, timeout=None):
        raise urllib.error.HTTPError(
            url="https://api.resend.com/emails", code=422,
            msg="Unprocessable", hdrs=None,
            fp=__import__("io").BytesIO(b'{"message": "domain not verified"}'),
        )

    monkeypatch.setattr("nstp.email.urllib.request.urlopen", http_error)
    with pytest.raises(urllib.error.HTTPError):
        send_mail("s", "b", "noreply@x.com", ["user@x.com"])


def test_missing_api_key_is_reported(settings, monkeypatch):
    settings.EMAIL_BACKEND = BACKEND
    settings.RESEND_API_KEY = ""
    settings.EMAIL_FAIL_SILENTLY = False
    # Never reaches the network — fails on the missing key.
    monkeypatch.setattr("nstp.email.urllib.request.urlopen",
                        lambda *a, **k: pytest.fail("should not call the API"))
    with pytest.raises(ValueError):
        send_mail("s", "b", "noreply@x.com", ["user@x.com"])


def test_missing_key_is_swallowed_when_silent(settings, monkeypatch):
    settings.EMAIL_BACKEND = BACKEND
    settings.RESEND_API_KEY = ""
    settings.EMAIL_FAIL_SILENTLY = True
    assert send_mail("s", "b", "noreply@x.com", ["user@x.com"]) == 0
