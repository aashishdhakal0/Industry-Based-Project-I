"""Certificate issuing, PDF, QR, and public verification.

Guards the integrity rules: a certificate is issued only from real completion
records, the PDF generates as a real PDF, the QR encodes the correct public
verification URL, and the verify page confirms genuine codes while rejecting
invalid ones.
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from certificates import pdf, services
from certificates.models import Certificate
from modules import gamification as g
from modules.models import Module
from quizzes.models import Quiz, QuizResult

User = get_user_model()


@pytest.fixture
def seeded(db):
    User.objects.create_user(
        email="cert-owner@example.com", password="x" * 14, is_superuser=True, is_staff=True
    )
    call_command("seed_learning_content")


def _finish_all(user, *, score=95):
    """Complete every lesson and pass every module quiz, from real records."""
    for module in Module.objects.all():
        for lesson in module.lessons.all():
            g.complete_lesson(user, lesson)
        QuizResult.objects.create(
            user=user, quiz=Quiz.objects.get(module=module),
            attempt_number=1, score=score, passed=True,
        )
    g.refresh_profile(user)


# --- issuing only on genuine completion ------------------------------------


@pytest.mark.django_db
def test_not_issued_until_every_module_is_complete(seeded):
    user = User.objects.create_user(email="learner@example.com", password="x" * 14, is_verified=True)
    assert services.completion(user).earned is False
    assert services.issue_for(user) is None
    assert Certificate.objects.count() == 0

    # Finish everything but the last module's quiz.
    modules = list(Module.objects.order_by("order_index"))
    for module in modules:
        for lesson in module.lessons.all():
            g.complete_lesson(user, lesson)
    for module in modules[:-1]:
        QuizResult.objects.create(user=user, quiz=Quiz.objects.get(module=module),
                                  attempt_number=1, score=90, passed=True)
    g.refresh_profile(user)
    assert services.issue_for(user) is None, "must not issue while a quiz is unpassed"
    assert Certificate.objects.count() == 0

    # Pass the last quiz: now it issues, exactly once.
    QuizResult.objects.create(user=user, quiz=Quiz.objects.get(module=modules[-1]),
                              attempt_number=1, score=90, passed=True)
    g.refresh_profile(user)
    cert = services.issue_for(user)
    assert cert is not None
    assert services.issue_for(user).pk == cert.pk, "issuing is idempotent"
    assert Certificate.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_serial_is_formatted_and_stable(seeded):
    user = User.objects.create_user(email="s@example.com", password="x" * 14, is_verified=True)
    _finish_all(user)
    cert = services.issue_for(user)
    assert cert.serial.startswith("CYB-")
    assert len(cert.serial) == 18 and cert.serial.count("-") == 3
    assert cert.serial == Certificate.serial_from_code(cert.code)


@pytest.mark.django_db
@pytest.mark.parametrize("score,expected", [(96, "Distinction"), (84, "Merit"), (72, "Pass")])
def test_grade_bands_from_real_scores(seeded, score, expected):
    user = User.objects.create_user(email=f"g{score}@example.com", password="x" * 14, is_verified=True)
    _finish_all(user, score=score)
    grade, avg = services.overall_grade(user)
    assert avg == score and grade == expected
    assert services.issue_for(user).grade == expected


# --- PDF --------------------------------------------------------------------


@pytest.mark.django_db
def test_pdf_renders_as_a_real_pdf(seeded, tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(email="pdf@example.com", password="x" * 14,
                                    first_name="Priya", last_name="Sharma", is_verified=True)
    _finish_all(user)
    cert = services.issue_for(user)
    out = pdf.build_and_cache(cert, name="Priya Sharma", date_str="30 August 2026",
                              verify_url="https://testserver/verify/%s/" % cert.serial)
    assert out.exists()
    data = out.read_bytes()
    assert data[:5] == b"%PDF-" and len(data) > 1500
    cert.refresh_from_db()
    assert cert.pdf_path.endswith(".pdf")


@pytest.mark.django_db
def test_download_requires_completion(client, seeded, tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    user = User.objects.create_user(email="dl@example.com", password="x" * 14, is_verified=True)
    client.force_login(user)
    # Incomplete: no PDF, redirected back to the certificate page.
    resp = client.get(reverse("certificates:download"))
    assert resp.status_code == 302 and reverse("learn:certificate") in resp["Location"]
    assert Certificate.objects.count() == 0

    _finish_all(user)
    resp = client.get(reverse("certificates:download"))
    assert resp.status_code == 200
    assert resp["Content-Type"] == "application/pdf"
    assert b"".join(resp.streaming_content)[:5] == b"%PDF-"


# --- QR + verification URL --------------------------------------------------


@pytest.mark.django_db
def test_qr_encodes_the_public_verify_url(seeded, rf):
    user = User.objects.create_user(email="qr@example.com", password="x" * 14, is_verified=True)
    _finish_all(user)
    cert = services.issue_for(user)
    request = rf.get("/learn/certificate/")
    verify_url = services.verify_url(request, cert.serial)
    # The URL the QR is built from must resolve back to this certificate.
    assert verify_url.endswith(reverse("certificates:verify", args=[cert.serial]))
    matrix = services.qr_matrix(verify_url)
    assert len(matrix) >= 21 and any(any(row) for row in matrix)
    svg = services.qr_svg(verify_url)
    assert svg.startswith("<svg") and "<path" in svg


@pytest.mark.django_db
def test_certificate_page_shows_real_serial_qr_and_download(client, seeded):
    user = User.objects.create_user(email="page@example.com", password="x" * 14,
                                    first_name="Sam", last_name="Lee", is_verified=True)
    client.force_login(user)
    _finish_all(user)
    html = client.get(reverse("learn:certificate")).content.decode()
    cert = Certificate.objects.get(user=user)
    assert cert.serial in html
    assert reverse("certificates:download") in html
    assert reverse("certificates:verify", args=[cert.serial]) in html
    assert "<svg" in html and "Sam Lee" in html


@pytest.mark.django_db
def test_certificate_page_is_locked_preview_before_completion(client, seeded):
    user = User.objects.create_user(email="lock@example.com", password="x" * 14, is_verified=True)
    client.force_login(user)
    html = client.get(reverse("learn:certificate")).content.decode()
    assert "not yet earned" in html.lower()
    assert reverse("certificates:download") not in html
    assert Certificate.objects.count() == 0


# --- public verify page -----------------------------------------------------


@pytest.mark.django_db
def test_verify_confirms_a_genuine_certificate(client, seeded):
    user = User.objects.create_user(email="v@example.com", password="x" * 14,
                                    first_name="Dana", last_name="Ng", is_verified=True)
    _finish_all(user)
    cert = services.issue_for(user)
    resp = client.get(reverse("certificates:verify", args=[cert.serial]))
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "Certificate verified" in html
    assert "Dana Ng" in html
    assert services.CREDENTIAL in html
    assert cert.serial in html


@pytest.mark.django_db
def test_verify_is_public_and_rejects_invalid_codes(client, seeded):
    # No login required.
    resp = client.get(reverse("certificates:verify", args=["CYB-0000-0000-0000"]))
    assert resp.status_code == 404
    html = resp.content.decode()
    assert "not found" in html.lower()
    assert "CYB-0000-0000-0000" in html


@pytest.mark.django_db
def test_verify_is_case_insensitive(client, seeded):
    user = User.objects.create_user(email="ci@example.com", password="x" * 14, is_verified=True)
    _finish_all(user)
    cert = services.issue_for(user)
    resp = client.get(reverse("certificates:verify", args=[cert.serial.lower()]))
    assert resp.status_code == 200
    assert "Certificate verified" in resp.content.decode()
