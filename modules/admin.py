"""Admin for training content."""

from django.contrib import admin

from .models import Lesson, Module, ProgressRecord, Simulation


class LessonInline(admin.TabularInline):
    """The four lessons, edited alongside their module."""

    model = Lesson
    extra = 0
    fields = ("lesson_number", "title", "reading_time_minutes", "is_active")
    ordering = ("lesson_number",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "order_index",
        "title",
        "difficulty",
        "duration_minutes",
        "is_published",
    )
    list_filter = ("difficulty", "is_published")
    search_fields = ("title", "description")
    ordering = ("order_index",)
    inlines = [LessonInline]
    list_select_related = ("created_by",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "module",
        "lesson_number",
        "title",
        "reading_time_minutes",
        "is_active",
    )
    list_filter = ("is_active", "module")
    search_fields = ("title", "body_text")
    list_select_related = ("module",)
    ordering = ("module__order_index", "lesson_number")


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ("module",)
    list_select_related = ("module",)


@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    list_filter = ("completed_at", "lesson__module")
    search_fields = ("user__email", "lesson__title")
    list_select_related = ("user", "lesson", "lesson__module")
    readonly_fields = ("completed_at",)
    date_hierarchy = "completed_at"
