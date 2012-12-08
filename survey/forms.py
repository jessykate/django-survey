from django import forms
from django.forms import models
from survey.models import Question, Category, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple
from django.utils.safestring import mark_safe
import uuid

# blatantly stolen from 
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


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

		# add a field for each survey question, corresponding to the question
		# type as appropriate.
		data = kwargs.get('data')
		for q in survey.questions():
			if q.question_type == Question.TEXT:
				self.fields["question_%d" % q.pk] = forms.CharField(label=q.text, 
					widget=forms.Textarea)
			elif q.question_type == Question.RADIO:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text, 
					widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), 
					choices = question_choices)
			elif q.question_type == Question.SELECT:
				question_choices = q.get_choices()
				# add an empty option at the top so that the user has to
				# explicitly select one of the options
				question_choices = tuple([('', '-------------')]) + question_choices
				self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text, 
					widget=forms.Select, choices = question_choices)
			elif q.question_type == Question.SELECT_MULTIPLE:
				question_choices = q.get_choices()
				self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.text, 
					widget=forms.CheckboxSelectMultiple, choices = question_choices)
			elif q.question_type == Question.INTEGER:
				self.fields["question_%d" % q.pk] = forms.IntegerField(label=q.text)				
			
			# if the field is required, give it a corresponding css class.
			if q.required:
				self.fields["question_%d" % q.pk].required = True
				self.fields["question_%d" % q.pk].widget.attrs["class"] = "required"
			else:
				self.fields["question_%d" % q.pk].required = False
				
			# add the category as a css class, and add it as a data attribute
			# as well (this is used in the template to allow sorting the
			# questions by category)
			if q.category:
				classes = self.fields["question_%d" % q.pk].widget.attrs.get("class")
				if classes:
					self.fields["question_%d" % q.pk].widget.attrs["class"] = classes + (" cat_%s" % q.category.name)
				else:
					self.fields["question_%d" % q.pk].widget.attrs["class"] = (" cat_%s" % q.category.name)
				self.fields["question_%d" % q.pk].widget.attrs["category"] = q.category.name


			# initialize the form field with values from a POST request, if any.
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





