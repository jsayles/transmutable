# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import datetime
import calendar
import pprint
import traceback

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
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import feedgenerator
from django.core.urlresolvers import reverse

from models import *
from forms import *

def index(request):
	if request.method == 'POST' and request.user.is_authenticated():
		namespace_form = NamespaceForm(request.POST, instance=Namespace(owner=request.user))
		if namespace_form.is_valid():
			namespace = namespace_form.save()
			return HttpResponseRedirect(namespace.get_absolute_url())
	else:
		namespace_form = NamespaceForm(instance=Namespace(owner=request.user))
	return render_to_response('peach/index.html', { 'users': User.objects.all(), 'namespace_form':namespace_form }, context_instance=RequestContext(request))

def namespace(request, namespace):
	ns = get_object_or_404(Namespace, name=namespace)
	page = WikiPage.objects.get_or_create(namespace__name=namespace, name='SplashPage')[0]
	if request.method == 'POST' and request.user.is_authenticated() and ns.owner == request.user:
		create_wiki_page_form = CreateWikiPageForm(request.POST, instance=WikiPage(namespace=ns))
		if create_wiki_page_form.is_valid():
			page = create_wiki_page_form.save()
			return HttpResponseRedirect(page.get_absolute_url())
	else:
		create_wiki_page_form = CreateWikiPageForm(instance=WikiPage(namespace=ns))
	return render_to_response('peach/namespace.html', { 'namespace':ns, 'create_wiki_page_form':create_wiki_page_form, 'wiki_pages':WikiPage.objects.filter(namespace__name=namespace).exclude(name='SplashPage'), 'page':page }, context_instance=RequestContext(request))

def photo_redirect(request, id):
	photo = get_object_or_404(WikiPhoto, pk=id)
	return HttpResponseRedirect(photo.image.url)

def photo_detail_redirect(request, id):
	photo = get_object_or_404(WikiPhoto, pk=id)
	return HttpResponseRedirect(photo.get_absolute_url())

def photo(request, name, id):
	photo = get_object_or_404(WikiPhoto, wiki_page__name=name, pk=id)
	return render_to_response('peach/photo.html', { 'photo':photo }, context_instance=RequestContext(request))

def file(request, namespace, name, id):
	file = get_object_or_404(WikiFile, wiki_page__name=name, pk=id)
	return render_to_response('peach/file.html', { 'file':file }, context_instance=RequestContext(request))

def wiki(request, namespace, name):
	if request.user.is_authenticated():
		ns = get_object_or_404(Namespace, name=namespace)
		if ns.owner == request.user:
			page, created = WikiPage.objects.get_or_create(namespace__name=namespace, name=name)
			if created or page.content == '': return HttpResponseRedirect(page.get_edit_url())
		else:
			page = get_object_or_404(WikiPage, namespace__name=namespace, name=name)
	else:
		page = get_object_or_404(WikiPage, namespace__name=namespace, name=name)
	return render_to_response('peach/wiki.html', { 'page':page }, context_instance=RequestContext(request))

def wiki_print(request, namespace, name):
	page = WikiPage.objects.get_or_create(namespace__name=namespace, name=name)[0]
	if request.user.is_authenticated and not page.id: return HttpResponseRedirect(page.get_edit_url())
	return render_to_response('peach/wiki_print.html', { 'page':page }, context_instance=RequestContext(request))

@login_required
def wiki_print_all(request):
	return render_to_response('peach/wiki_print_all.html', { 'pages':WikiPage.objects.all() }, context_instance=RequestContext(request))

@login_required
def wiki_add(request, namespace, name):
	ns = get_object_or_404(Namespace, name=namespace)
	if request.user != ns.owner: return HttpResponseRedirect('peaches.views.wiki', kwargs={'namespace':namespace, 'name':name})
	page = WikiPage.objects.get_or_create(namespace__name=namespace, name=name)[0]
	if request.method == 'POST':
		if request.user != ns.owner: return HttpResponseRedirect('peaches.views.index')
		wiki_photo_form = WikiPhotoForm(request.POST, request.FILES)
		wiki_file_form = WikiFileForm(request.POST, request.FILES)
		if request.POST.get('photo-form', None):
			wiki_file_form = WikiFileForm()
			if wiki_photo_form.is_valid():
				photo = wiki_photo_form.save(commit=False)
				if not page.id: page.save()
				photo.wiki_page = page
				photo.save()
				page.content = "%s\n\nPhoto%s" % (page.content, photo.id)
				page.save()
				return HttpResponseRedirect(page.get_edit_url())
		elif request.POST.get('file-form', None):
			wiki_photo_form = WikiPhotoForm()
			if wiki_file_form.is_valid():
				file = wiki_file_form.save(commit=False)
				if not page.id: page.save()
				file.wiki_page = page
				file.save()
				return HttpResponseRedirect(page.get_edit_url())
		else:
			print request.POST
	else:
		wiki_photo_form = WikiPhotoForm()
		wiki_file_form = WikiFileForm()
	return render_to_response('peach/wiki_add.html', { 'page':page, 'wiki_photo_form':wiki_photo_form, 'wiki_file_form':wiki_file_form }, context_instance=RequestContext(request))

@login_required
def wiki_history(request, namespace, name):
	return render_to_response('peach/wiki_history.html', { 'page':WikiPage.objects.get_or_create(namespace__name=namespace, name=name)[0] }, context_instance=RequestContext(request))

@login_required
def wiki_page_log(request, namespace, name, id):
	page_log = get_object_or_404(WikiPageLog, wiki_page__name=name, pk=id)
	ns = get_object_or_404(Namespace, name=namespace)
	if request.method == 'POST' and request.POST.get('revert', None):
		if request.user != ns.owner: return HttpResponseRedirect(page_log.get_absolute_url())
		page_log.wiki_page.content = page_log.content
		page_log.wiki_page.save()
		return HttpResponseRedirect(page_log.wiki_page.get_absolute_url())
	return render_to_response('peach/wiki_page_log.html', { 'page_log':page_log  }, context_instance=RequestContext(request))

@login_required
def wiki_edit(request, namespace, name):
	ns = get_object_or_404(Namespace, name=namespace)
	if request.user != ns.owner: return HttpResponseRedirect(reverse('peach.views.namespace', kwargs={'namespace':namespace}))
	page = WikiPage.objects.get_or_create(namespace__name=namespace, name=name)[0]
	if request.method == 'POST':
		page_form = WikiPageForm(request.POST, instance=page)
		if page_form.is_valid():
			page = page_form.save()
			if request.GET.get('next', None): return HttpResponseRedirect(request.GET.get('next'))
			return HttpResponseRedirect(page.get_absolute_url())
	else:
		page_form = WikiPageForm(instance=page)
	return render_to_response('peach/wiki_edit.html', { 'page':page, 'page_form':page_form }, context_instance=RequestContext(request))
