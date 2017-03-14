from django.conf.urls import include, url
from django.contrib import admin

from survey.views import confirm, index, survey_detail

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^survey/(?P<id>\d+)/$', survey_detail, name='survey_detail'),
    url(r'^confirm/(?P<uuid>\w+)/$', confirm, name='confirmation'),
    url(r'^admin/', include(admin.site.urls)),
]
