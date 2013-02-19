from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.gif'}, name='favicon'),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^backbone/', include('backbone.urls', app_name='backbone')),
	url(r'^api/backbone/', include('backbone.api_urls', app_name='backbone_api')),
	url(r'^api/notes/', include('peach.api_urls', app_name='peach_api')),

	url(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/p/profile/'}, name='profile'),
	url(r'^accounts/login/$', 'django.views.generic.simple.redirect_to', {'url': '/p/login/'}, name='login'),

	url(r'^p/', include('person.urls', app_name='person')),
	url(r'^notes/', include('peach.urls', app_name='peach')),
	url(r'^staff/', include('apple.urls', app_name='apple')),
	url(r'^', include('banana.urls', app_name='banana')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
