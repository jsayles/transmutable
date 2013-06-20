import calendar
import pprint
import traceback
import urllib
import simplejson as json
from datetime import datetime, timedelta, date

from dynamicresponse.json_response import JsonResponse

from django.db.models import Q
from django.contrib import auth
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.utils.html import urlize
from django.core.mail import send_mail
from django.utils import feedgenerator
from django.utils.html import strip_tags
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Context, loader
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import django.contrib.contenttypes.models as content_type_models
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from models import CompletedItem, CompletedItemRock, Gratitude
from peach.forms import NamespaceForm

def index(request):
	day_limit = 4
	context = {
		'promoted_users': User.objects.exclude(profile__bio='').exclude(profile__bio=None).exclude(profile__mute=True).order_by('?'),
		'completed_items': CompletedItem.objects.recent(max_count=10, created_after=datetime.now() - timedelta(days=day_limit), exclude_users_younger_than=timezone.now() - timedelta(days=day_limit + 1)),
		'gratitudes': Gratitude.objects.recent(max_count=10, created_after=datetime.now() - timedelta(days=day_limit),  exclude_users_younger_than=timezone.now() - timedelta(days=day_limit + 1))
	}
	return render_to_response('banana/index.html', context, context_instance=RequestContext(request))

def activity(request):
	'''A timely snapshot of what's going on around the site.'''
	day_limit = 20
	context = {
		'completed_items': CompletedItem.objects.recent(max_count=100, created_after=datetime.now() - timedelta(days=day_limit)),
		'gratitudes': Gratitude.objects.recent(max_count=100, created_after=datetime.now() - timedelta(days=day_limit))
	}
	return render_to_response('banana/activity.html', context, context_instance=RequestContext(request))

@login_required
def user_redirect(request):
	return HttpResponseRedirect(request.user.get_absolute_url())

def user(request, username):
	user = get_object_or_404(User, username=username)
	if request.user == user and not request.GET.get('public') == 'true':
		return render_to_response('banana/user.html', {'user':user }, context_instance=RequestContext(request))
	else:
		return render_to_response('banana/user_public.html', { 'user':user }, context_instance=RequestContext(request))

def gratitude(request, id):
	gratitude = get_object_or_404(Gratitude, pk=id)
	return render_to_response('banana/gratitude.html', {'gratitude':gratitude}, context_instance=RequestContext(request))

def completed_item(request, id):
	item = get_object_or_404(CompletedItem, pk=id)
	return render_to_response('banana/completed_item.html', { 'completed_item':item, }, context_instance=RequestContext(request))

# Copyright 2011-2013 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
