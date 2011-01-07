import datetime
import calendar
import pprint
import traceback
import urllib

from django.utils.html import urlize
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.template import Context, loader
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
import django.contrib.contenttypes.models as content_type_models
from django.template import RequestContext
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator
from django.utils.encoding import smart_str

from models import *
from forms import WorkDocForm

def index(request):
	return render_to_response('banana/index.html', { 'users':User.objects.all().order_by('-work_docs__modified') }, context_instance=RequestContext(request))

def user(request, username):
	user = get_object_or_404(User, username=username)
	return render_to_response('banana/user.html', { 'user':user, }, context_instance=RequestContext(request))

def edit_workdoc(request, username):
	user = get_object_or_404(User, username=username)
	if request.method == 'POST':
		workdoc_form = WorkDocForm(request.POST)
		if workdoc_form.is_valid():
			user.work_doc.save_markup(workdoc_form.cleaned_data['markup'])
			return HttpResponseRedirect(reverse('banana.views.user', kwargs={ 'username':user.username }))
	else:
		workdoc_form = WorkDocForm(instance=user.work_doc)
	return render_to_response('banana/edit_workdoc.html', { 'user':user, 'workdoc_form':workdoc_form }, context_instance=RequestContext(request))
