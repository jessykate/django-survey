import uuid
import logging

from django import forms
from django.forms import models
from django.core.urlresolvers import reverse

from survey.models import Question, Response
from survey.models import AnswerText, AnswerRadio, AnswerSelect
from survey.models import AnswerInteger, AnswerSelectMultiple
from survey.widgets import ImageSelectWidget
from survey.signals import survey_completed

from django.utils.safestring import mark_safe

# blatantly stolen from 
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class ResponseForm(models.ModelForm):
    class Meta:
        model = Response    
        fields = ()

    def __init__(self, *args, **kwargs):
        # expects a survey object to be passed in initially
        survey = kwargs.pop('survey')
        self.survey = survey
        self.user = kwargs.pop('user')
        try:
            self.step = int(kwargs.pop('step'))
        except KeyError:
            self.step = None

        
        super(ResponseForm, self).__init__(*args, **kwargs)
        random_uuid = uuid.uuid4().hex
        self.uuid = random_uuid
        
        self.steps_count = survey.questions().count()
        
        # add a field for each survey question, corresponding to the question
        # type as appropriate.
        data = kwargs.get('data')
        for index, q in enumerate(survey.questions()):
            if self.survey.display_by_question and index != self.step and self.step is not None:
                continue
            else:
                if q.question_type == Question.TEXT:
                    self.fields["question_%d" % q.pk] = forms.CharField(label=q.text, 
                        widget=forms.Textarea)
                elif q.question_type == Question.SHORT_TEXT:
                    self.fields["question_%d" % q.pk] = forms.CharField(label=q.text, 
                        widget=forms.TextInput)
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
                elif q.question_type == Question.SELECT_IMAGE:
                    question_choices = q.get_choices()
                    # add an empty option at the top so that the user has to
                    # explicitly select one of the options
                    question_choices = tuple([('', '-------------')]) + question_choices
                    self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text, 
                        widget=ImageSelectWidget, choices = question_choices)
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
                    self.fields["question_%d" % q.pk].widget.attrs["required"] = True
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

                if q.question_type == Question.SELECT:
                    classes = self.fields["question_%d" % q.pk].widget.attrs.get("class")
                    self.fields["question_%d" % q.pk].widget.attrs["class"] = classes + (" cs-select cs-skin-boxes")

                if q.question_type == Question.RADIO:
                    classes = self.fields["question_%d" % q.pk].widget.attrs.get("class")
                    self.fields["question_%d" % q.pk].widget.attrs["class"] = classes + (" fs-radio-group fs-radio-custom clearfix")

                #if q.question_type == Question.SELECT_MULTIPLE:
                #    classes = self.fields["question_%d" % q.pk].widget.attrs.get("class")
                #    self.fields["question_%d" % q.pk].widget.attrs["class"] = classes + (" ")

                # initialize the form field with values from a POST request, if any.
                if data:
                    self.fields["question_%d" % q.pk].initial = data.get('question_%d' % q.pk)

    def has_next_step(self):
        if self.survey.display_by_question:
            if self.step < self.steps_count-1:
                return True
        return False

    def next_step_url(self):
        if self.has_next_step():
            return reverse('survey-detail-step', kwargs={'id':self.survey.id, 'step': self.step+1})
        else:
            return None

    def current_step_url(self):
        return reverse('survey-detail-step', kwargs={'id':self.survey.id, 'step': self.step})

    def save(self, commit=True):
        # save the response object
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.interview_uuid = self.uuid
        if self.user.is_authenticated():
            response.user = self.user
        response.save()

        # response "raw" data as dict (for signal)
        data = {
            'survey_id': response.survey.id,
            'interview_uuid': response.interview_uuid,
            'responses': []
        }
        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in the
                # field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)
                
                if q.question_type == Question.TEXT or q.question_type == Question.SHORT_TEXT:
                    a = AnswerText(question = q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question = q)   
                    a.body = field_value
                elif q.question_type == Question.SELECT:
                    a = AnswerSelect(question = q)  
                    a.body = field_value
                elif q.question_type == Question.SELECT_IMAGE:
                    a = AnswerSelect(question = q)
                    value, img_src = field_value.split(":", 1)
                    a.body = value
                elif q.question_type == Question.SELECT_MULTIPLE:
                    a = AnswerSelectMultiple(question = q)  
                    a.body = field_value
                elif q.question_type == Question.INTEGER:   
                    a = AnswerInteger(question = q) 
                    a.body = field_value
                data['responses'].append((a.question.id, a.body))
                logging.debug("creating answer to question %d of type %s" % (q_id, a.question.question_type))
                logging.debug(a.question.text)
                logging.debug('answer value:')
                logging.debug(field_value)

                a.response = response
                a.save()
        survey_completed.send(sender=Response, instance=response, data=data)
        return response

