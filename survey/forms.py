from django import forms
from django.forms import models
from survey.models import Question, Category, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple

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

		# add a field for each question associated with this survey,
		# corresponding to the question type as appropriate.

		data = kwargs.get('data')
		for q in survey.questions():
			if q.question_type == Question.TEXT:
				if q.category:
					cat = q.category.id 
				else: cat = 0
				self.fields["question_%d" % q.pk] = forms.CharField(label=q.text, 
				widget=forms.Textarea(attrs={"class": "category_%d" % cat}))
			elif q.question_type == Question.RADIO:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text, 
					widget=forms.RadioSelect, choices = question_choices)
			elif q.question_type == Question.SELECT:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text, 
					widget=forms.Select, choices = question_choices)
			elif q.question_type == Question.SELECT_MULTIPLE:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.text, 
					widget=forms.CheckboxSelectMultiple, choices = question_choices)
			elif q.question_type == Question.INTEGER:
				self.fields["question_%d" % q.pk] = forms.IntegerField(label=q.text)				
			
			if not q.required:
				print "question __%s__ is not required" % q.text
				self.fields["question_%d" % q.pk].required = False

			# initialize the form field with values from a POST request, if
			# any.
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
				# warning: this way of extracting the id is very fragile and
				# entirely dependent on the way the question_id is encoded in the
				# field name in the __init__ method of this form class.
				q_id = int(field_name.split("_")[1])
				q = Question.objects.get(pk=q_id)
				
				if q.question_type == Question.TEXT:
					a = AnswerText(question = q)
					a.body = field_value
				elif q.question_type == Question.RADIO:
					a = AnswerRadio(question = q)	
					a.body = field_value
				elif q.question_type == Question.SELECT:
					a = AnswerSelect(question = q)	
					a.body = field_value
				elif q.question_type == Question.SELECT_MULTIPLE:
					a = AnswerSelectMultiple(question = q)	
					a.body = field_value
				elif q.question_type == Question.INTEGER:	
					a = AnswerInteger(question = q)	
					a.body = field_value
				print "creating answer to question %d of type %s" % (q_id, a.question.question_type) 
				print a.question.text
				print 'answer value:'
				print field_value
				a.response = response
				a.save()
		return response





