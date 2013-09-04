from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Survey, Category
from .forms import ResponseForm


from django.views.generic import TemplateView, View

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['surveys'] = Survey.objects.filter(is_published=True)
        return context


class SurveyDetail(View):
    template_name = 'survey.html'

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        category_items = Category.objects.filter(survey=survey)
        categories = [c.name for c in category_items]
        form = ResponseForm(survey=survey)
        context = {'response_form': form, 'survey': survey, 'categories': categories}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        category_items = Category.objects.filter(survey=survey)
        categories = [c.name for c in category_items]
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)

        context = {'response_form': form, 'survey': survey, 'categories': categories}
        return render(request, self.template_name, context)

class ConfirmView(TemplateView):
    template_name = 'confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context['uuid'] = kwargs['uuid']
        return context
