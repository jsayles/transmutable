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

from forms import WikiPageForm, NamespaceForm, CreateWikiPageForm
from models import Namespace, WikiPage

@login_required
def index(request):
	if request.method == 'POST':
		namespace_form = NamespaceForm(request.POST, instance=Namespace(owner=request.user))
		if namespace_form.is_valid():
			if Namespace.objects.filter(owner=request.user, display_name=namespace_form.cleaned_data['display_name']).count() > 0:
				return HttpResponseRedirect(Namespace.objects.get(owner=request.user, display_name=namespace_form.cleaned_data['display_name']).get_absolute_url())
			namespace = namespace_form.save()
			return HttpResponseRedirect(reverse('peach.mobile_views.namespace', kwargs={'namespace':namespace.name}))
	else:
		namespace_form = NamespaceForm(instance=Namespace(owner=request.user))
	
	return render_to_response('peach/mobile/index.html', {'namespace_form':namespace_form}, context_instance=RequestContext(request))

@login_required
def namespace(request, namespace):
	ns = get_object_or_404(Namespace, owner=request.user, name=namespace)
	page = WikiPage.objects.get_or_create(namespace=ns, name='SplashPage')[0]
	if request.method == 'POST' and ns.can_update(request.user):
		create_wiki_page_form = CreateWikiPageForm(request.POST, instance=WikiPage(namespace=ns))
		if create_wiki_page_form.is_valid() and WikiPage.objects.filter(namespace=ns, name=create_wiki_page_form.cleaned_data['name']).count() == 0:
			page = create_wiki_page_form.save()
			return HttpResponseRedirect(reverse('peach.mobile_views.wiki_edit', kwargs={'namespace':namespace, 'name':page.name}))
	else:
		create_wiki_page_form = CreateWikiPageForm(instance=WikiPage(namespace=ns))
	if not ns.can_read(request.user): return HttpResponseRedirect(reverse('peach.mobile_views.index'))
	return render_to_response('peach/mobile/namespace.html', { 'namespace':ns, 'page':page, 'create_wiki_page_form':create_wiki_page_form, 'wiki_pages':WikiPage.objects.filter(namespace=ns).exclude(name='SplashPage') }, context_instance=RequestContext(request))

@login_required
def wiki(request, namespace, name):
	ns = get_object_or_404(Namespace, owner=request.user, name=namespace)
	if not ns.can_read(request.user): return HttpResponseRedirect(reverse('peach.mobile_views.index'))
	page, created = WikiPage.objects.get_or_create(namespace=ns, name=name)
	if created or page.content == '': return HttpResponseRedirect(reverse('peach.mobile_views.wiki_edit', kwargs={'namespace':namespace, 'name':name}))
	return render_to_response('peach/mobile/wiki.html', { 'page':page }, context_instance=RequestContext(request))


@login_required
def wiki_edit(request, namespace, name):
	ns = get_object_or_404(Namespace, owner=request.user, name=namespace)
	if not ns.can_update(request.user): return HttpResponseRedirect(reverse('peach.mobile_views.namespace', kwargs={'namespace':namespace}))
	page = WikiPage.objects.get_or_create(namespace=ns, name=name)[0]
	if request.method == 'POST':
		page_form = WikiPageForm(request.POST, instance=page)
		if page_form.is_valid():
			page = page_form.save()
			if request.GET.get('next', None): return HttpResponseRedirect(request.GET.get('next'))
			return HttpResponseRedirect(page.get_mobile_url())
	else:
		page_form = WikiPageForm(instance=page)
	return render_to_response('peach/mobile/wiki_edit.html', { 'page':page, 'page_form':page_form }, context_instance=RequestContext(request))
