from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'person/login.html'}),
	(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/' }),

	(r'^register/$', 'person.views.register'),
	(r'^invite/$', 'person.views.invites'),
	(r'^invite/(?P<secret>[^/]+)/$', 'person.views.invite'),
	(r'^profile/$', 'person.views.profile_redirect'),
	(r'^find/$', 'person.views.find_people'),
	(r'^password-reset/$', 'person.views.password_reset'),
	(r'^email-validate/(?P<username>[^/]+)/(?P<secret>[^/]+)/$', 'person.views.email_validate'),
	(r'^edit/photo/$', 'person.views.photo_edit'),
	(r'^edit/password/$', 'person.views.password_edit'),
	(r'(?P<username>[^/]+)/$' , 'person.views.profile'),
)