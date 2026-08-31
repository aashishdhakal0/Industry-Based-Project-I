"""Certificate download (PDF) and public verification."""

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from . import pdf, services
from .models import Certificate


def _award_date(cert):
    return timezone.localtime(cert.issued_at).strftime("%-d %B %Y")


@login_required
def download(request):
    """Serve the certificate PDF, generating and caching it on first request.

    Issues strictly from real records: `issue_for` returns None unless every
    module is complete, so an incomplete learner cannot download a credential.
    """
    cert = services.issue_for(request.user)
    if cert is None:
        return redirect("learn:certificate")
    name = request.user.get_full_name() or request.user.email
    verify_url = services.verify_url(request, cert.serial)
    out = pdf.build_and_cache(
        cert, name=name, date_str=_award_date(cert), verify_url=verify_url
    )
    return FileResponse(
        open(out, "rb"),
        as_attachment=True,
        filename=f"Cybaroo-Certificate-{cert.serial}.pdf",
        content_type="application/pdf",
    )


def verify(request, serial):
    """Public page (no login) confirming a certificate is genuine.

    A valid serial shows the recipient, credential, grade and date; an unknown
    serial renders a clear 'not found' state and a 404 status.
    """
    cert = (
        Certificate.objects.select_related("user")
        .filter(serial__iexact=serial)
        .first()
    )
    if cert is None:
        return render(
            request,
            "certificates/verify.html",
            {"valid": False, "serial": serial},
            status=404,
        )
    user = cert.user
    return render(
        request,
        "certificates/verify.html",
        {
            "valid": True,
            "serial": cert.serial,
            "recipient": user.get_full_name() or user.email,
            "credential": services.CREDENTIAL,
            "grade": cert.grade,
            "issued": timezone.localtime(cert.issued_at),
        },
    )
