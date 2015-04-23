from django.conf.urls import patterns, url

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'survey.views.Index', name='home'),
	url(r'^survey/(?P<id>\d+)/$', 'survey.views.SurveyDetail', name='survey_detail'),
	url(r'^confirm/(?P<uuid>\w+)/$', 'survey.views.Confirm', name='confirmation'),
)
