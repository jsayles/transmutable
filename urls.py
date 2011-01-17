from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse

admin.autodiscover()

urlpatterns = patterns('',
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/favicon.gif'}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

	(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
	(r'^accounts/login/$', 'django.views.generic.simple.redirect_to', {'url': '/p/login/'}),

    (r'^p/', include('person.urls')),
    (r'^notes/', include('peach.urls')),
    (r'^', include('banana.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
