from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'banana.views.index'),
    (r'^u/(?P<username>[^/]+)/$', 'banana.views.user'),
)