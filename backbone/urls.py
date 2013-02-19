from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^search/$', 'backbone.views.search'),
	(r'^url/$', 'backbone.views.urls'),
)
