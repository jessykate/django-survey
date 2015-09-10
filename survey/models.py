from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .utils import validate_list


class Survey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    is_published = models.BooleanField()
    need_logged_user = models.BooleanField()
    display_by_question = models.BooleanField()
    template = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')

    def __unicode__(self):
        return (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('survey-detail', [self.id])

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk).order_by('category__order', 'order')
        else:
            return Question.objects.none()


class Category(models.Model):
    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return (self.name)


class Question(models.Model):
    TEXT = 'text'
    SHORT_TEXT = 'short-text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_IMAGE = 'select_image'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, _(u'text (multiple line)')),
        (SHORT_TEXT, _(u'short text (one line)')),
        (RADIO, _(u'radio')),
        (SELECT, _(u'select')),
        (SELECT_MULTIPLE, _(u'Select Multiple')),
        (SELECT_IMAGE, _(u'Select Image')),
        (INTEGER, _(u'integer')),
    )

    text = models.TextField()
    order = models.IntegerField()
    required = models.BooleanField()
    category = models.ForeignKey(Category, blank=True, null=True,) 
    survey = models.ForeignKey(Survey)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    # the choices field is only used if the question type 
    choices = models.TextField(blank=True, null=True,
        help_text=_(u"if the question type is 'radio', 'select', or 'select multiple' provide a comma-separated list of options for this question ."))

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ('survey', 'order')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT 
            or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        """
        Parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.
        """
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c,c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        return (self.text)


class Response(models.Model):
    """
    A Response object is just a collection of questions and answers with a
    unique interview uuid
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User, null=True, blank=True)
    interview_uuid = models.CharField(_(u"Interview unique identifier"), max_length=36)

    class Meta:
        verbose_name = _('response')
        verbose_name_plural = _('responses')

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
