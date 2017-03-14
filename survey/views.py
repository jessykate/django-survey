import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from survey.forms import ResponseForm
from survey.models import Category, Survey

LOGGER = logging.getLogger(__name__)


def index(request):
    surveys = Survey.objects.all()
    return render(request, 'survey/index.html', {'surveys': surveys})


def survey_detail(request, id):
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    LOGGER.info('Categories for this survey: %s', categories)
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
    else:
        form = ResponseForm(survey=survey)
        LOGGER.info(form)
        # TODO sort by category
    return render(
        request, 'survey/survey.html',
        {'response_form': form, 'survey': survey, 'categories': categories}
    )


def confirm(request, uuid):
    email = settings.SUPPORT_EMAIL
    return render(request, 'confirm.html', {'uuid': uuid, "email": email})
