from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'banana.views.index'),
	(r'^edit/workdoc/$', 'banana.views.workdoc_edit'),
	(r'^edit/completed/$', 'banana.views.completed_edit'),
	(r'^edit/user/$', 'banana.views.user_edit'),
	(r'^u/(?P<username>[^/]+)/$', 'banana.views.user'),
)