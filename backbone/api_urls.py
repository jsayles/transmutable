from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^backbone.js$', 'backbone.api_views.backbone_js'),
	(r'^site/$', 'backbone.api_views.site'),
	(r'^search/$', 'backbone.api_views.search'),
)
