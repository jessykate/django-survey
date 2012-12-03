from django.db import models

class Survey(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField()

	def __unicode__(self):
		return (self.name)

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return None

class Category(models.Model):
	name = models.CharField(max_length=400)
	survey = models.ForeignKey(Survey)

	def __unicode__(self):
		return (self.name)


class Question(models.Model):
	text = models.TextField()
	required = models.BooleanField()
	category = models.ForeignKey(Category, blank=True, null=True) # Choice field. 
	survey = models.ForeignKey(Survey)

	def __unicode__(self):
		return (self.text)

class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	survey = models.ForeignKey(Survey)
	interviewer = models.CharField(max_length=400)
	interviewee = models.CharField(max_length=400)
	conditions = models.TextField(blank=True, null=True)
	comments = models.TextField(blank=True, null=True)
	interview_uuid = models.CharField("Interview unique identifier", max_length=36)

	def __unicode__(self):
		return ("response %s" % self.interview_uuid)

class Answer(models.Model):
	question = models.ForeignKey(Question)
	response = models.ForeignKey(Response)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	#interview_uuid = models.CharField("Interview unique identifier", max_length=36)





