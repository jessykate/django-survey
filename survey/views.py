from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import Survey, Category
from .forms import ResponseForm


from django.views.generic import TemplateView, View

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        qs = Survey.objects.filter(is_published=True)
        if not self.request.user.is_authenticated():
            qs = qs.filter(need_logged_user=False)
        context['surveys'] = qs
        return context


class SurveyDetail(View):
    template_name = 'survey.html'

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        if survey.need_logged_user and not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        category_items = Category.objects.filter(survey=survey)
        categories = [c.name for c in category_items]
        form = ResponseForm(survey=survey, user=request.user)
        context = {'response_form': form, 'survey': survey, 'categories': categories}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        if survey.need_logged_user and not request.user.is_authenticated():
            return redirect('/login/?next=%s' % request.path)
        category_items = Category.objects.filter(survey=survey)
        categories = [c.name for c in category_items]
        form = ResponseForm(request.POST, survey=survey, user=request.user)
        if form.is_valid():
            response = form.save()
            return redirect('survey-confirmation', uuid=response.interview_uuid)

        context = {'response_form': form, 'survey': survey, 'categories': categories}
        return render(request, self.template_name, context)


class ConfirmView(TemplateView):
    template_name = 'confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context['uuid'] = kwargs['uuid']
        return context
