from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'banana.views.index'),
    (r'^u/(?P<username>[^/]+)/$', 'banana.views.user'),
    (r'^u/(?P<username>[^/]+)/edit-workdoc/$', 'banana.views.edit_workdoc'),
)