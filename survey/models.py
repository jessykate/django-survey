from django.db import models

from .utils import validate_list

class Survey(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField()
	is_published = models.BooleanField()

	def __unicode__(self):
		return (self.name)

	@models.permalink
	def get_absolute_url(self):
		return ('survey-detail', [self.id])

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return Question.objects.none()


class Category(models.Model):
	name = models.CharField(max_length=400)
	survey = models.ForeignKey(Survey)

	def __unicode__(self):
		return (self.name)


class Question(models.Model):
	TEXT = 'text'
	SHORT_TEXT = 'short-text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'

	QUESTION_TYPES = (
		(TEXT, 'text (multiple line)'),
		(SHORT_TEXT, 'short text (one line)'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)

	text = models.TextField()
	order = models.IntegerField()
	required = models.BooleanField()
	category = models.ForeignKey(Category, blank=True, null=True,) 
	survey = models.ForeignKey(Survey)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
	# the choices field is only used if the question type 
	choices = models.TextField(blank=True, null=True,
		help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')

	def save(self, *args, **kwargs):
		if (self.question_type == Question.RADIO or self.question_type == Question.SELECT 
			or self.question_type == Question.SELECT_MULTIPLE):
			validate_list(self.choices)
		super(Question, self).save(*args, **kwargs)

	def get_choices(self):
		''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
		choices = self.choices.split(',')
		choices_list = []
		for c in choices:
			c = c.strip()
			choices_list.append((c,c))
		choices_tuple = tuple(choices_list)
		return choices_tuple

	def __unicode__(self):
		return (self.text)

	class Meta:
		ordering = ('survey', 'order')


class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	survey = models.ForeignKey(Survey)
	interview_uuid = models.CharField("Interview unique identifier", max_length=36)

	def __unicode__(self):
		return ("response %s" % self.interview_uuid)


class AnswerBase(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerRadio(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelect(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerSelectMultiple(AnswerBase):
	body = models.TextField(blank=True, null=True)

class AnswerInteger(AnswerBase):
	body = models.IntegerField(blank=True, null=True)
