"""Admin for training content."""

from django.contrib import admin

from .models import (
    Lesson,
    LessonTask,
    Module,
    ProgressRecord,
    Simulation,
    SimulationResult,
    TaskProgress,
)


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


@admin.register(LessonTask)
class LessonTaskAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order", "task_key", "kind", "points")
    list_filter = ("kind", "lesson__module")
    search_fields = ("task_key", "title", "body")
    list_select_related = ("lesson", "lesson__module")
    ordering = ("lesson__module__order_index", "lesson__lesson_number", "order")


@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "completed_at")
    list_filter = ("completed_at",)
    search_fields = ("user__email", "task__task_key")
    list_select_related = ("user", "task", "task__lesson")
    readonly_fields = ("completed_at",)


@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    list_filter = ("completed_at", "lesson__module")
    search_fields = ("user__email", "lesson__title")
    list_select_related = ("user", "lesson", "lesson__module")
    readonly_fields = ("completed_at",)
    date_hierarchy = "completed_at"


@admin.register(SimulationResult)
class SimulationResultAdmin(admin.ModelAdmin):
    list_display = ("user", "simulation", "score", "total", "completed_at")
    list_filter = ("completed_at", "simulation__module")
    search_fields = ("user__email",)
    list_select_related = ("user", "simulation", "simulation__module")
    readonly_fields = ("completed_at",)
    date_hierarchy = "completed_at"
