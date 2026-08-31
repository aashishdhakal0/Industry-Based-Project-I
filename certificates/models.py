"""Completion certificates."""

import uuid

from django.conf import settings
from django.db import models


class Certificate(models.Model):
    """Issued once a student has passed all six module quizzes.

    `code` is the public verification identifier — anyone can check it against
    the database to confirm a certificate is genuine.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates"
    )
    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Internal verification identifier.",
    )
    serial = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Public, human-readable verification code (CYB-XXXX-XXXX-XXXX).",
    )
    grade = models.CharField(
        max_length=20,
        blank=True,
        help_text="Overall academic grade at issue (Distinction / Merit / Pass).",
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_path = models.CharField(
        max_length=500, blank=True, help_text="Path to the generated PDF under MEDIA_ROOT."
    )

    class Meta:
        db_table = "certificates"
        ordering = ["-issued_at"]

    def __str__(self):
        return f"Certificate {self.serial} — {self.user.email}"

    @staticmethod
    def serial_from_code(code):
        """Derive the public serial from the UUID: CYB-XXXX-XXXX-XXXX."""
        h = code.hex.upper()
        return f"CYB-{h[:4]}-{h[4:8]}-{h[8:12]}"

    def save(self, *args, **kwargs):
        if not self.serial:
            self.serial = self.serial_from_code(self.code)
        super().save(*args, **kwargs)
