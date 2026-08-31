"""Certificate issuing, grading, verification, and QR generation.

Everything here is driven from real records: a certificate is only issued once
`modules.gamification.module_progress` shows every module complete (server-side,
never trusting the client), and the grade is computed from the learner's own quiz
scores. The QR code is produced with ReportLab's built-in encoder, so there is no
extra dependency and nothing leaves our origin.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.db.models import Max
from django.urls import reverse

from modules import gamification as g
from quizzes.models import QuizResult

from .models import Certificate

# The credential this certificate attests to. One place, so the on-screen page,
# the PDF, and the verification page never drift apart.
CREDENTIAL = "Cyber Safety Essentials"
CREDENTIAL_SUBTITLE = "the complete cyber safety program for Australian workplaces"

# Academic grade bands, by the average of the learner's best score in each module.
_GRADE_BANDS = [(90, "Distinction"), (80, "Merit"), (70, "Pass")]


@dataclass
class Completion:
    earned: bool
    done: int
    total: int

    @property
    def percent(self) -> int:
        return round(self.done / self.total * 100) if self.total else 0


def completion(user) -> Completion:
    """Real completion state from the progress records."""
    prog = list(g.module_progress(user))
    done = sum(1 for mp in prog if mp.complete)
    total = len(prog)
    return Completion(earned=total > 0 and done >= total, done=done, total=total)


def _best_scores(user) -> list[int]:
    """The learner's best PASSED score in each module that has a quiz."""
    rows = (
        QuizResult.objects.filter(user=user, passed=True)
        .values("quiz__module")
        .annotate(best=Max("score"))
    )
    return [r["best"] for r in rows]


def overall_grade(user) -> tuple[str | None, int | None]:
    """Average the best passed score per module and map it to a grade band.

    Returns (grade, average). Grade is None if the learner has not passed
    anything yet; when the course is complete it is always at least 'Pass'.
    """
    scores = _best_scores(user)
    if not scores:
        return None, None
    avg = round(sum(scores) / len(scores))
    for floor, name in _GRADE_BANDS:
        if avg >= floor:
            return name, avg
    return None, avg


def issue_for(user) -> Certificate | None:
    """Issue (or return the existing) certificate, only on genuine completion.

    Idempotent: one certificate per learner. Returns None if the course is not
    finished, so callers can never mint a credential for incomplete work.
    """
    if not completion(user).earned:
        return None
    cert, created = Certificate.objects.get_or_create(user=user)
    grade, _avg = overall_grade(user)
    if grade and cert.grade != grade:
        cert.grade = grade
        cert.save(update_fields=["grade"])
    return cert


# --- verification ----------------------------------------------------------


def verify_path(serial: str) -> str:
    return reverse("certificates:verify", args=[serial])


def verify_url(request, serial: str) -> str:
    """Absolute URL to the public verification page (used by the QR + printout)."""
    return request.build_absolute_uri(verify_path(serial))


# --- QR code ---------------------------------------------------------------


def qr_matrix(data: str) -> list[list[bool]]:
    """The QR modules as a boolean grid, via ReportLab's built-in encoder."""
    from reportlab.graphics.barcode import qr

    widget = qr.QrCodeWidget(data)
    widget.qr.make()
    n = widget.qr.getModuleCount()
    return [[bool(widget.qr.isDark(r, c)) for c in range(n)] for r in range(n)]


def qr_svg(data: str, *, dark: str = "#1f3350", light: str = "#ffffff", quiet: int = 4) -> str:
    """A crisp, self-contained inline SVG QR for the on-screen certificate."""
    matrix = qr_matrix(data)
    n = len(matrix)
    size = n + quiet * 2
    parts = []
    for r, row in enumerate(matrix):
        for c, on in enumerate(row):
            if on:
                parts.append(f"M{c + quiet} {r + quiet}h1v1h-1z")
    path = "".join(parts)
    return (
        f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" '
        f'shape-rendering="crispEdges" role="img" '
        f'aria-label="QR code to verify this certificate">'
        f'<rect width="{size}" height="{size}" fill="{light}"/>'
        f'<path d="{path}" fill="{dark}"/></svg>'
    )
