"""Admin for completion certificates."""

from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "issued_at", "pdf_path")
    search_fields = ("code", "user__email")
    list_select_related = ("user",)
    # `code` is editable=False on the model; issued_at is auto_now_add.
    readonly_fields = ("issued_at",)
    date_hierarchy = "issued_at"
