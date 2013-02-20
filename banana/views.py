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
from forms import WorkDocForm, CompletedItemForm, RockCompletedItemForm, GratitudeForm
from peach.forms import NamespaceForm

def index(request):
	day_limit = 4
	promoted_users = User.objects.exclude(profile__bio='').exclude(profile__bio=None).order_by('?')
	return render_to_response('banana/index.html', {'promoted_users':promoted_users, 'completed_items':CompletedItem.objects.recent(max_count=10, created_after=datetime.now() - timedelta(days=day_limit)), 'users':User.objects.filter(work_docs__modified__gt=datetime.now() - timedelta(days=day_limit)).order_by('-work_docs__modified') }, context_instance=RequestContext(request))

@staff_member_required
def test(request):
	if not settings.DEBUG: raise Http404
	return render_to_response('banana/tests.html', { }, context_instance=RequestContext(request))

@login_required
def user_redirect(request):
	return HttpResponseRedirect(request.user.get_absolute_url())

def user(request, username):
	user = get_object_or_404(User, username=username)
	if request.user == user and not request.GET.get('public') == 'true':
		workdoc_form = WorkDocForm(instance=user.work_doc)
		completed_form = CompletedItemForm(instance=CompletedItem(user=request.user))
		return render_to_response('banana/user.html', {'workdoc_form':workdoc_form, 'completed_form':completed_form, 'namespace_form':NamespaceForm(), 'user':user }, context_instance=RequestContext(request))
	else:
		return render_to_response('banana/user_public.html', { 'user':user }, context_instance=RequestContext(request))

def gratitude(request, id):
	gratitude = get_object_or_404(Gratitude, pk=id)
	if request.method == 'PUT':
		gratitude_form = GratitudeForm(request.POST, instance=gratitude)
		if gratitude_form.is_valid():
			gratitude = gratitude_form.save()
			return JsonResponse(gratitude.flatten())
		else:
			return HttpResponse(status=400)
	return render_to_response('banana/gratitude.html', {'gratitude':gratitude}, context_instance=RequestContext(request))

@login_required
def gratitudes(request):
	if request.method == 'POST':
		gratitude_form = GratitudeForm(request.POST, instance=Gratitude(user=request.user))
		if gratitude_form.is_valid():
			gratitude = gratitude_form.save()
			return JsonResponse(gratitude.flatten())
		else:
			return HttpResponse(status=400)
	return JsonResponse([gratitude.flatten() for gratitude in request.user.gratitudes.all()[:20]])

def completed_item(request, id):
	item = get_object_or_404(CompletedItem, pk=id)
	if request.method == 'PUT':
		item_form = CompletedItemForm(request.POST, instance=item)
		if item_form.is_valid():
			item = item_form.save()
			return JsonResponse(item.flatten())
		else:
			print request.POST, item_form
			return HttpResponse(status=400)
	return render_to_response('banana/completed_item.html', { 'completed_item':item, }, context_instance=RequestContext(request))

@login_required
def completed_items(request):
	if request.method == 'POST':
		create_form = CompletedItemForm(request.POST, instance=CompletedItem(user=request.user))
		if create_form.is_valid():
			item = create_form.save()
			return JsonResponse(item.flatten())
		else:
			print request.POST, create_form
			return HttpResponse(status=400)
	return JsonResponse([item.flatten() for item in request.user.completed_items.all()[:20]])

@login_required
def completed_item_rock(request):
	if request.method == 'POST':
		rock_completed_item_form = RockCompletedItemForm(request.POST)
		if rock_completed_item_form.is_valid():
			completed_item = get_object_or_404(CompletedItem, pk=rock_completed_item_form.cleaned_data['completed_item_id'])
			rock, created = CompletedItemRock.objects.get_or_create(completed_item=completed_item, user=request.user)
			flat_rock = rock.flatten()
			flat_rock['created'] = created
			return JsonResponse(flat_rock)
		else:
			print request.POST, create_form
			return HttpResponse(status=400)
	raise HttpResponseServerError('Error')

@login_required
def workdoc_edit(request):
	if request.method == 'POST':
		workdoc_form = WorkDocForm(request.POST)
		if workdoc_form.is_valid():
			request.user.work_doc.save_markup(workdoc_form.cleaned_data['markup'])
	return HttpResponse(json.dumps(request.user.work_doc.flatten()), mimetype='application/json')

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
