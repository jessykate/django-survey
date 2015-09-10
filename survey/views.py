from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings

from .models import Survey, Category, Response
from .forms import ResponseForm


from django.views.generic import TemplateView, View


class IndexView(TemplateView):
    template_name = "survey/list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        qs = Survey.objects.filter(is_published=True)
        if not self.request.user.is_authenticated():
            qs = qs.filter(need_logged_user=False)
        context['surveys'] = qs
        return context


class SurveyDetail(View):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.display_by_question:
                template_name = 'survey/survey.html'
            else:
                template_name = 'survey/one_page_survey.html'
        if survey.need_logged_user and not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if survey.need_logged_user and request.user.is_authenticated():
            if Response.objects.filter(survey=survey, user=request.user).exists():
                return redirect('survey-completed', id=survey.id)

        category_items = Category.objects.filter(survey=survey).order_by('order')
        categories = [c.name for c in category_items]
        form = ResponseForm(survey=survey, user=request.user, step=kwargs.get('step', 0))
        context = {
            'response_form': form,
            'survey': survey,
            'categories': categories,
        }

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        if survey.need_logged_user and not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if survey.need_logged_user and request.user.is_authenticated():
            if Response.objects.filter(survey=survey, user=request.user).exists():
                return redirect('survey-completed', id=survey.id)
        category_items = Category.objects.filter(survey=survey).order_by('order')
        categories = [c.name for c in category_items]
        form = ResponseForm(request.POST, survey=survey, user=request.user, step=kwargs.get('step', 0))
        context = {'response_form': form, 'survey': survey, 'categories': categories}
        if form.is_valid():
            session_key = 'survey_%s' % (kwargs['id'],)
            if not session_key in request.session:
                request.session[session_key] = {}
            for key, value in form.cleaned_data.items():
                request.session[session_key][key] = value
                request.session.modified = True

            next_url = form.next_step_url()
            response = None
            if survey.display_by_question:
                if not form.has_next_step():
                    save_form = ResponseForm(request.session[session_key], survey=survey, user=request.user)
                    response = save_form.save()
            else:
                response = form.save()

            if next_url is not None:
                return redirect(next_url)
            else:
                del request.session[session_key]
                if response is None:
                    return redirect('/')
                else:
                    next = request.session.get('next', None)
                    if next is not None:
                        if 'next' in request.session:
                            del request.session['next']
                        return redirect(next)
                    else:
                        return redirect('survey-confirmation', uuid=response.interview_uuid)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.display_by_question:
                template_name = 'survey/survey.html'
            else:
                template_name = 'survey/one_page_survey.html'
        return render(request, template_name, context)


class ConfirmView(TemplateView):
    template_name = 'survey/confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context['uuid'] = kwargs['uuid']
        return context


class SurveyCompleted(TemplateView):
    template_name = 'survey/completed.html'

    def get_context_data(self, **kwargs):
        context = super(SurveyCompleted, self).get_context_data(**kwargs)
        survey = get_object_or_404(Survey, is_published=True, id=kwargs['id'])
        context['survey'] = survey
        return context
