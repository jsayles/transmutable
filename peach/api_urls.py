from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^namespace/$', 'peach.api_views.namespaces'),
	(r'^namespace/(?P<name>[^/]+)/$', 'peach.api_views.namespace'),

	(r'^namespace-pages/(?P<name>[^/]+)/$', 'peach.api_views.pages'),
	(r'^page/(?P<id>[\d]+)/$', 'peach.api_views.page'),
)
