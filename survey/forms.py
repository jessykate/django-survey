from django import forms
from django.forms import models
from survey.models import Response, Answer, Question
import uuid

# one field from each question
# when saving, one answer object for each question. 

# class AnswerForm(models.ModelForm):
# 	class Meta:
# 		model = Answer 
# 		include = ['text']

# 	def __init__(self, *args, **kwargs):
# 		question = kwargs.pop('question')
# 		super(AnswerForm, self).__init__(*args, **kwargs)
# 		question_text = question.text
# 		self.fields.label = question_text

# 	def save(self, commit=True):
# 		ans = super(AnswerForm, self).save(commit=False)
# 		ans.question = question
# 		ans.save()

class ResponseForm(models.ModelForm):
	class Meta:
		model = Response	
		fields = ('interviewer', 'interviewee', 'conditions', 'comments')

	def __init__(self, *args, **kwargs):
		# expects a survey object to be passed in initially
		survey = kwargs.pop('survey')
		self.survey = survey
		super(ResponseForm, self).__init__(*args, **kwargs)
		self.uuid = random_uuid = uuid.uuid4().hex	

		# add a field for each question associated with this survey
		for q in survey.questions():
			self.fields["question_%d" % q.pk] = forms.CharField(label=q.text, widget=forms.Textarea)
			if not q.required:
				self.fields["question_%d" % q.pk].required = False

			# initialize the form fields with values from a POST request, if any.  	
			data = kwargs.get('data')
			if data:
				self.fields["question_%d" % q.pk].initial = data.get('question_%d' % q.pk)


	def save(self, commit=True):
		# save the response object
		response = super(ResponseForm, self).save(commit=False)
		response.survey = self.survey
		response.interview_uuid = self.uuid
		response.save()

		# create an answer object for each question and associate it with this
		# response.
		for field_name, field_value in self.cleaned_data.iteritems():
			if field_name.startswith("question_"):
				a = Answer()
				# this way of extracting the id is very fragile and entirely
				# dependent on the way the question_id is encoded in the field
				# name in the __init__ method of this form class.
				q_id = int(field_name.split("_")[1])
				print "creating answer to question %d" % q_id 
				a.question = Question.objects.get(pk=q_id)
				print a.question.text
				print 'answer value:'
				print field_value
				a.text = field_value
				a.response = response
				a.save()
		return response





