import datetime
import calendar
import pprint
import traceback
import urllib
import simplejson as json

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

from models import CompletedItem, CompletedItemRock, WorkDoc
from forms import WorkDocForm, CompletedItemForm, RockCompletedItemForm
from peach.forms import NamespaceForm

@login_required
def index(request): #aka to-do
	return render_to_response('banana/mobile/index.html', { }, context_instance=RequestContext(request))

@login_required
def activity(request):
	return render_to_response('banana/mobile/activity.html', {  'completed_items':CompletedItem.objects.recent(max_count=10, created_after=datetime.datetime.now() - datetime.timedelta(days=4)) }, context_instance=RequestContext(request))

@login_required
def notes(request):
	return render_to_response('banana/mobile/notes.html', { }, context_instance=RequestContext(request))

@login_required
def todone(request):
	if request.method == 'POST':
		completed_form = CompletedItemForm(request.POST, instance=CompletedItem(user=request.user))
		if completed_form.is_valid():
			item = completed_form.save()
			completed_form = CompletedItemForm(instance=CompletedItem(user=request.user))
		else:
			print 'not valid'
	else:
		completed_form = CompletedItemForm(instance=CompletedItem(user=request.user))
	return render_to_response('banana/mobile/todone.html', { 'completed_form':completed_form }, context_instance=RequestContext(request))

@login_required
def todo_edit(request):
	if request.method == 'POST':
		workdoc_form = WorkDocForm(request.POST)
		if workdoc_form.is_valid():
			request.user.work_doc.save_markup(workdoc_form.cleaned_data['markup'])
			return HttpResponseRedirect(reverse('banana.mobile_views.index'))
	else:
		workdoc_form = WorkDocForm(instance=request.user.work_doc)
	return render_to_response('banana/mobile/todo_edit.html', { 'workdoc_form':workdoc_form }, context_instance=RequestContext(request))