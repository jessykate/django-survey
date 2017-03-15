
from django.contrib import admin

from survey.models import (AnswerInteger, AnswerRadio, AnswerSelect,
                           AnswerSelectMultiple, AnswerText, Category,
                           Question, Response, Survey)


class QuestionInline(admin.TabularInline):
    model = Question
    ordering = ('category',)
    extra = 0


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, QuestionInline]


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
    list_display = ('interview_uuid', 'created')
    inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline,
               AnswerSelectMultipleInline, AnswerIntegerInline]
    # specifies the order as well as which fields to act on
    readonly_fields = ('survey', 'created', 'updated', 'interview_uuid')

# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)

admin.site.register(Response, ResponseAdmin)
