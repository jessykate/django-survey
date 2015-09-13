from django.contrib import admin

from .models import Question, Category, Survey, Response, AnswerText
from .models import AnswerRadio, AnswerSelect
from .models import AnswerInteger, AnswerSelectMultiple
from .actions import make_published


class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('category', 'order',)
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'need_logged_user', 'template')
    list_filter = ('is_published', 'need_logged_user')
    inlines = [CategoryInline, QuestionInline]
    actions = [make_published]


class AnswerBaseInline(admin.StackedInline):
    fields = ('question', 'body')
    readonly_fields = ('question',)
    extra = 0


class AnswerTextInline(AnswerBaseInline):
    model = AnswerText


class AnswerRadioInline(AnswerBaseInline):
    model = AnswerRadio


class AnswerSelectInline(AnswerBaseInline):
    model = AnswerSelect


class AnswerSelectMultipleInline(AnswerBaseInline):
    model = AnswerSelectMultiple


class AnswerIntegerInline(AnswerBaseInline):
    model = AnswerInteger


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('interview_uuid', 'survey', 'created', 'user')
    list_filter = ('survey', 'created')
    date_hierarchy = 'created'
    inlines = [
        AnswerTextInline, AnswerRadioInline, AnswerSelectInline,
        AnswerSelectMultipleInline, AnswerIntegerInline
    ]
    # specifies the order as well as which fields to act on
    readonly_fields = (
        'survey', 'created', 'updated', 'interview_uuid', 'user'
    )


# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Response, ResponseAdmin)
