"""Render a certificate to a print-quality PDF with ReportLab.

A4 landscape, the classic Times serif (a built-in PDF font, so nothing to embed
and it stays sharp at any print size), a gold double frame, an engraved seal, and
a QR code drawn from the same matrix the on-screen page uses. Generated lazily and
cached under MEDIA_ROOT/certificates/.
"""

from __future__ import annotations

import math
from pathlib import Path

from django.conf import settings
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from . import services, signature

PAPER = HexColor("#fbf7ec")
INK = HexColor("#23252b")
MUTED = HexColor("#74705f")
NAVY = HexColor("#1f3350")
GOLD = HexColor("#a6842f")
GOLD_LT = HexColor("#caa85f")

PAGE = landscape(A4)  # (841.89, 595.28) points
W, H = PAGE


def _tracked(c, x, y, text, font, size, color, tracking=0.0, centred=True):
    """Draw letter-spaced text (ReportLab has no CSS letter-spacing)."""
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [c.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    cx = x - total / 2 if centred else x
    for ch, w in zip(text, widths):
        c.drawString(cx, y, ch)
        cx += w + tracking


def _arc_text(c, cx, cy, radius, text, font, size, color, center_deg, spread_deg, flip=False):
    """Lay text along a circular arc, centred on center_deg."""
    c.setFont(font, size)
    c.setFillColor(color)
    n = len(text)
    if n == 1:
        angles = [center_deg]
    else:
        step = spread_deg / (n - 1)
        angles = [center_deg + spread_deg / 2 - i * step for i in range(n)]
    for ch, ang in zip(text, angles):
        rad = math.radians(ang)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        c.saveState()
        c.translate(x, y)
        rot = ang - 90 if not flip else ang + 90
        c.rotate(rot)
        c.drawCentredString(0, 0, ch)
        c.restoreState()


def _seal(c, cx, cy, r):
    c.setLineWidth(1.2)
    c.setStrokeColor(GOLD_LT)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.6)
    c.circle(cx, cy, r - 4.5, stroke=1, fill=0)
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(0.8)
    c.circle(cx, cy, r - 10.5, stroke=1, fill=0)
    _arc_text(c, cx, cy, r - 7, "CYBAROO", "Times-Bold", 6.4, HexColor("#7d6321"), 90, 84)
    _arc_text(c, cx, cy, r - 7, "CYBER SAFETY PROGRAM", "Times-Bold", 6.0,
              HexColor("#7d6321"), 270, 120, flip=True)
    # shield
    s = r * 0.44
    c.setFillColor(NAVY)
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(1.3)
    p = c.beginPath()
    p.moveTo(cx, cy + s)
    p.lineTo(cx + s * 0.72, cy + s * 0.42)
    p.lineTo(cx + s * 0.72, cy - s * 0.35)
    p.curveTo(cx + s * 0.72, cy - s * 0.9, cx + s * 0.3, cy - s * 1.15, cx, cy - s * 1.3)
    p.curveTo(cx - s * 0.3, cy - s * 1.15, cx - s * 0.72, cy - s * 0.9, cx - s * 0.72, cy - s * 0.35)
    p.lineTo(cx - s * 0.72, cy + s * 0.42)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    # tick
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(2.6)
    c.setLineCap(1)
    c.setLineJoin(1)
    t = c.beginPath()
    t.moveTo(cx - s * 0.34, cy - s * 0.05)
    t.lineTo(cx - s * 0.08, cy - s * 0.34)
    t.lineTo(cx + s * 0.4, cy + s * 0.34)
    c.drawPath(t, stroke=1, fill=0)


def _frame(c):
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.4)
    c.rect(26, 26, W - 52, H - 52, stroke=1, fill=0)
    c.setStrokeColor(GOLD_LT)
    c.setLineWidth(0.8)
    c.rect(32, 32, W - 64, H - 64, stroke=1, fill=0)
    # corner ticks
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    for (x, y, dx, dy) in [(26, 26, 1, 1), (W - 26, 26, -1, 1),
                           (26, H - 26, 1, -1), (W - 26, H - 26, -1, -1)]:
        c.line(x + dx * 14, y + dy * 14, x + dx * 30, y + dy * 14)
        c.line(x + dx * 14, y + dy * 14, x + dx * 14, y + dy * 30)


def _qr(c, matrix, x, y, box):
    n = len(matrix)
    c.setFillColor(HexColor("#ffffff"))
    pad = box
    c.rect(x - pad, y - pad, n * box + pad * 2, n * box + pad * 2, stroke=0, fill=1)
    c.setFillColor(NAVY)
    for r, row in enumerate(matrix):
        for col, on in enumerate(row):
            if on:
                c.rect(x + col * box, y + (n - 1 - r) * box, box, box, stroke=0, fill=1)


def render_bytes(*, name, credential, credential_sub, grade, date_str, serial, verify_url):
    """Draw the certificate and return the PDF as bytes."""
    import io

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=PAGE)
    c.setTitle(f"Cybaroo Certificate — {name}")

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _frame(c)

    cx = W / 2
    _tracked(c, cx, H - 70, "CYBAROO", "Times-Bold", 15, NAVY, tracking=3)
    _tracked(c, cx, H - 86, "CYBER SAFETY TRAINING", "Times-Roman", 8, HexColor("#3a5075"), tracking=4)

    _seal(c, cx, H - 138, 34)

    _tracked(c, cx, H - 196, "CERTIFICATE OF COMPLETION", "Times-Bold", 22, NAVY, tracking=6)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(cx - 70, H - 210, cx + 70, H - 210)

    c.setFont("Times-Italic", 12)
    c.setFillColor(MUTED)
    c.drawCentredString(cx, H - 236, "This certificate is proudly presented to")

    _tracked(c, cx, H - 288, name, "Times-Bold", 40, INK, tracking=0.5)
    c.setStrokeColor(HexColor("#3a5075"))
    c.setLineWidth(0.8)
    c.line(cx - 150, H - 300, cx + 150, H - 300)

    c.setFont("Times-Roman", 12)
    c.setFillColor(MUTED)
    c.drawCentredString(cx, H - 326, "for successfully completing all six modules and assessments of the")

    _tracked(c, cx, H - 360, credential, "Times-Bold", 24, NAVY, tracking=1)
    c.setFont("Times-Italic", 11)
    c.setFillColor(MUTED)
    c.drawCentredString(cx, H - 378, credential_sub)

    if grade:
        _tracked(c, cx, H - 414, f"AWARDED WITH {grade.upper()}", "Times-Bold", 13,
                 HexColor("#7d6321"), tracking=4)

    # ---- footer: QR + code (left), date (centre), signature (right) ----
    matrix = services.qr_matrix(verify_url)
    box = 2.0
    qn = len(matrix)
    qx = 92
    qy = 66
    _qr(c, matrix, qx, qy, box)
    tx = qx + qn * box + 16
    _tracked(c, tx, qy + qn * box - 4, "VERIFY AUTHENTICITY", "Times-Roman", 7.5, MUTED,
             tracking=2, centred=False)
    c.setFont("Times-Bold", 12)
    c.setFillColor(NAVY)
    c.drawString(tx, qy + qn * box - 22, serial)
    c.setFont("Times-Roman", 8.5)
    c.setFillColor(HexColor("#3a3b40"))
    c.drawString(tx, qy + qn * box - 36, verify_url)

    c.setFont("Times-Bold", 13)
    c.setFillColor(INK)
    c.drawCentredString(cx, 92, date_str)
    _tracked(c, cx, 78, "DATE OF AWARD", "Times-Roman", 7.5, MUTED, tracking=2)

    rx = W - 150
    # The hand-crafted signature flourish, drawn above the line (same geometry
    # as the on-screen mark), never a typed name.
    signature.draw(c, rx - 58, 103, 116, 44, color="#1f3350")
    c.setStrokeColor(HexColor("#3a3b40"))
    c.setLineWidth(0.8)
    c.line(rx - 70, 100, rx + 70, 100)
    c.setFont("Times-Roman", 9.5)
    c.setFillColor(HexColor("#3a3b40"))
    c.drawCentredString(rx, 86, "Issued by Cybaroo")
    _tracked(c, rx, 74, "DIRECTOR OF TRAINING", "Times-Roman", 7, MUTED, tracking=2)

    c.showPage()
    c.save()
    return buf.getvalue()


def path_for(cert) -> Path:
    return Path(settings.MEDIA_ROOT) / "certificates" / f"{cert.serial}.pdf"


def build_and_cache(cert, *, name, date_str, verify_url) -> Path:
    """Generate the PDF if not already cached, and record its path on the row."""
    out = path_for(cert)
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        data = render_bytes(
            name=name,
            credential=services.CREDENTIAL,
            credential_sub=services.CREDENTIAL_SUBTITLE,
            grade=cert.grade,
            date_str=date_str,
            serial=cert.serial,
            verify_url=verify_url,
        )
        out.write_bytes(data)
    rel = str(out.relative_to(settings.MEDIA_ROOT))
    if cert.pdf_path != rel:
        cert.pdf_path = rel
        cert.save(update_fields=["pdf_path"])
    return out
