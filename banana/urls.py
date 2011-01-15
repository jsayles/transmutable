from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'banana.views.index'),
	(r'^edit-workdoc/$', 'banana.views.edit_workdoc'),
	(r'^edit-completed/$', 'banana.views.edit_completed'),
	(r'^u/(?P<username>[^/]+)/$', 'banana.views.user'),
)