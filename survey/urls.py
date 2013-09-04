from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

from .views import IndexView, SurveyDetail, ConfirmView

admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = patterns('',
	# Examples:
	url(r'^$', IndexView.as_view(), name='survey-list'),
	url(r'^survey/(?P<id>\d+)/$', SurveyDetail.as_view(), name='survey-detail'),
	url(r'^confirm/(?P<uuid>\w+)/$', ConfirmView.as_view(), name='survey-confirmation'),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

# media url hackery. le sigh. 
urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
)

