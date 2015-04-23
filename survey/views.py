from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
import settings

from models import Question, Survey, Category
from forms import ResponseForm


def Index(request):
        surveys = Survey.objects.all()
	return render(request, 'survey/index.html', {'surveys': surveys})

def SurveyDetail(request, id):
	survey = Survey.objects.get(id=id)
	category_items = Category.objects.filter(survey=survey)
	categories = [c.name for c in category_items]
	print 'categories for this survey:'
	print categories
	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect(
                              urlresolvers.reverse('confirmation', kwargs={'uuid': response.interview_uuid}))
	else:
		form = ResponseForm(survey=survey)
		print form
		# TODO sort by category
	return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey, 'categories': categories})

def Confirm(request, uuid):
	email = settings.support_email
	return render(request, 'survey/confirm.html', {'uuid':uuid, "email": email})


