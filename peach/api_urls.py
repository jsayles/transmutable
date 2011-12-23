from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^namespace/$', 'peach.api_views.namespaces'),
	(r'^namespace/(?P<name>[^/]+)/$', 'peach.api_views.namespace'),
)
