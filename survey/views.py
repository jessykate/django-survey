# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from survey.forms import ResponseForm
from survey.models import Category, Survey


LOGGER = logging.getLogger(__name__)


def login_maybe_required(user):
    """ Check if the user is logged if settings.SURVEY_AUTH_REQUIRED is True.

    If it is not defined or False return True. """
    try:
        if not settings.SURVEY_AUTH_REQUIRED:
            return True
        return user.is_authenticated()
    except AttributeError:
        return True


@user_passes_test(login_maybe_required)
def index(request):
    surveys = Survey.objects.all()
    return render(request, 'survey/index.html', {'surveys': surveys})


@user_passes_test(login_maybe_required)
def survey_detail(request, id):
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    LOGGER.info('Categories for this survey: %s', categories)
    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey, user=request.user)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
    else:
        form = ResponseForm(survey=survey, user=request.user)
        LOGGER.info(form)
        # TODO sort by category
    return render(
        request, 'survey/survey.html',
        {'response_form': form, 'survey': survey, 'categories': categories}
    )


@user_passes_test(login_maybe_required)
def confirm(request, uuid):
    email = settings.SUPPORT_EMAIL
    return render(request, 'confirm.html', {'uuid': uuid, "email": email})
