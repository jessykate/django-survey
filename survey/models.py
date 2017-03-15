# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models


class Survey(models.Model):

    name = models.CharField(max_length=400)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('survey_detail', kwargs={'id': self.pk})


class Category(models.Model):

    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey, related_name="categories")

    def __unicode__(self):
        return self.name


def validate_list(value):
    '''takes a text value and verifies that there is at least one comma '''
    values = value.split(',')
    if len(values) < 2:
        msg = "The selected field requires an associated list of choices. "
        msg += "Choices must contain more than one item."
        raise ValidationError(msg)


class Question(models.Model):

    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'integer'),
    )

    text = models.TextField()
    required = models.BooleanField()
    category = models.ForeignKey(Category, related_name="questions",
                                 blank=True, null=True)
    survey = models.ForeignKey(Survey, related_name="questions")
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES,
                                     default=TEXT)

    choices = models.TextField(
        help_text="""The choices field is only used if the question type is
"radio," "select," or "select multiple". Provide a
comma-separated list of options for this question .""", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.question_type in [Question.RADIO, Question.SELECT,
                                  Question.SELECT_MULTIPLE]:
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.'''
        choices = str(self.choices).split(',')
        choices_list = []
        for choice in choices:
            choice = choice.strip()
            choices_list.append((choice, choice))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return self.text


class Response(models.Model):

    """ A response object is just a collection of questions and answers with a
    unique interview uuid """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)
    interview_uuid = models.CharField("Interview unique identifier",
                                      max_length=36)

    def __unicode__(self):
        return "Response {}".format(self.interview_uuid)


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
