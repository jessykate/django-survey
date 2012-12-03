from survey.models import Question, Category, Survey, Response, Answer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class QuestionInline(admin.TabularInline):
	model = Question
	ordering = ('category',)
	extra = 0

class CategoryInline(admin.TabularInline):
	model = Category
	extra = 0

class SurveyAdmin(admin.ModelAdmin):
	inlines = [CategoryInline, QuestionInline]

class AnswerInline(admin.StackedInline):
	model= Answer 
	fields = ('question', 'text')
	readonly_fields = ('question',)
	extra = 0

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('interview_uuid', 'interviewer', 'created') 
	inlines = [AnswerInline]
	# specifies the order as well as which fields to act on 
	readonly_fields = ('survey', 'created', 'updated', 'interview_uuid')

#admin.site.register(Question, QuestionInline)
#admin.site.register(Category, CategoryInline)
admin.site.register(Survey, SurveyAdmin)

admin.site.register(Response, ResponseAdmin)
