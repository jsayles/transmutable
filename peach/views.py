# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import traceback

from django.db.models import Q
from django.contrib import auth
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import feedgenerator
from django.utils.html import strip_tags
from django.template import RequestContext
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import django.contrib.contenttypes.models as content_type_models
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from transmutable import serialize_query_set

from models import *
from forms import *
from api import WikiPhotoResource

@login_required
def index(request):
	return render_to_response('peach/index.html', { }, context_instance=RequestContext(request))

def namespace(request, username, namespace):
	ns = get_object_or_404(Namespace, owner__username=username, name=namespace)
	if not ns.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	page = WikiPage.objects.get_or_create(namespace=ns, name='SplashPage')[0]
	if request.user == ns.owner and not request.GET.get('public') == 'true':
		return render_to_response('peach/namespace.html', { 'namespace':ns, 'wiki_pages':WikiPage.objects.filter(namespace=ns).exclude(name='SplashPage'), 'page':page }, context_instance=RequestContext(request))
	else:
		return render_to_response('peach/namespace_public.html', { 'namespace':ns, 'wiki_pages':WikiPage.objects.filter(namespace=ns).exclude(name='SplashPage'), 'page':page }, context_instance=RequestContext(request))
		
def photo_redirect(request, id):
	photo = get_object_or_404(WikiPhoto, pk=id)
	return HttpResponseRedirect(photo.image.url)

def photo_detail_redirect(request, id):
	photo = get_object_or_404(WikiPhoto, pk=id)
	return HttpResponseRedirect(photo.get_absolute_url())

def photo(request, name, id):
	photo = get_object_or_404(WikiPhoto, wiki_page__name=name, pk=id)
	if not photo.wiki_page.namespace.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	return render_to_response('peach/photo.html', { 'photo':photo }, context_instance=RequestContext(request))

def file(request, namespace, name, id):
	file = get_object_or_404(WikiFile, wiki_page__name=name, pk=id)
	if not file.wiki_page.namespace.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	return render_to_response('peach/file.html', { 'file':file }, context_instance=RequestContext(request))

def wiki(request, username, namespace, name):
	ns = get_object_or_404(Namespace, name=namespace, owner__username=username)
	page = get_object_or_404(WikiPage, namespace=ns, name=name)
	if not page.namespace.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))

	if request.method == 'POST':
		if not page.namespace.can_update(request.user):
			return HttpResponse('Not authed', status=403)
		wiki_photos_form = WikiPhotosForm(request.POST, request.FILES)
		if wiki_photos_form.is_valid():
			photos = wiki_photos_form.save(page, request.FILES)
			serialized_photos = serialize_query_set(photos, WikiPhotoResource, request)
			return HttpResponse(serialized_photos, status=200)
		else:
			print 'not valid', wiki_files_form
			return HttpResponse('Form not valid', status=400)

	return render_to_response('peach/wiki.html', { 'page':page }, context_instance=RequestContext(request))

def wiki_print(request, username, namespace, name):
	namespace = get_object_or_404(Namespace, name=namespace, owner__username=username)
	page = get_object_or_404(WikiPage, namespace=namespace, name=name)
	if not page.namespace.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	return render_to_response('peach/wiki_print.html', { 'page':page }, context_instance=RequestContext(request))

@login_required
def wiki_history(request, username, namespace, name):
	ns = get_object_or_404(Namespace, name=namespace, owner__username=username)
	if not ns.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	page = get_object_or_404(WikiPage, namespace=ns, name=name)
	return render_to_response('peach/wiki_history.html', { 'page':page }, context_instance=RequestContext(request))

@login_required
def wiki_page_log(request, username, namespace, name, id):
	page_log = get_object_or_404(WikiPageLog, wiki_page__name=name, pk=id)
	ns = get_object_or_404(Namespace, name=namespace, owner__username=username)
	if request.method == 'POST' and request.POST.get('revert', None):
		if not ns.can_update(request.user): return HttpResponseRedirect(page_log.get_absolute_url())
		page_log.wiki_page.content = page_log.content
		page_log.wiki_page.save()
		return HttpResponseRedirect(page_log.wiki_page.get_absolute_url())
	if not ns.can_read(request.user): return render_to_response('peach/not_authed.html', {}, context_instance=RequestContext(request))
	return render_to_response('peach/wiki_page_log.html', { 'page_log':page_log  }, context_instance=RequestContext(request))
