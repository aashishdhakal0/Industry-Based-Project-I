"""Admin for the quiz engine.

Answers are edited inline on their question: a question is only ever valid with
its full set of four options, so the two are authored together.
"""

from django.contrib import admin

from .models import Answer, Question, Quiz, QuizResult, WrongAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("option_text", "correct_answer", "explanation_text")


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("ordering", "question_text", "difficulty", "lesson_reference")
    ordering = ("ordering",)
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("module", "time_limit_minutes", "pass_mark", "is_active")
    list_filter = ("is_active",)
    list_select_related = ("module",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz", "difficulty", "lesson_reference")
    list_filter = ("difficulty", "quiz__module")
    search_fields = ("question_text",)
    list_select_related = ("quiz", "quiz__module", "lesson_reference")
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("option_text", "question", "correct_answer")
    list_filter = ("correct_answer",)
    search_fields = ("option_text", "explanation_text")
    list_select_related = ("question",)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "passed", "attempt_number", "submitted_at")
    list_filter = ("passed", "quiz__module", "submitted_at")
    search_fields = ("user__email",)
    list_select_related = ("user", "quiz", "quiz__module")
    readonly_fields = ("submitted_at",)
    date_hierarchy = "submitted_at"


@admin.register(WrongAnswer)
class WrongAnswerAdmin(admin.ModelAdmin):
    list_display = ("quiz_result", "question", "student_answer", "correct_answer")
    search_fields = ("question__question_text",)
    list_select_related = (
        "quiz_result",
        "quiz_result__user",
        "question",
        "student_answer",
        "correct_answer",
    )
