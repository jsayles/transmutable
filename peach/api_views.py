import datetime
import traceback

from django.db.models import Q
from django.contrib import auth
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from dynamicresponse.json_response import JsonResponse

from api_forms import NamespaceForm, CreateNamespaceForm, CreateWikiPageForm, WikiPageForm
from models import Namespace, WikiPage

def namespaces(request):
	if request.method == 'POST':
		if not Namespace.can_create(request.user): return HttpResponse(status=403)
		create_namespace_form = CreateNamespaceForm(request.POST, instance=Namespace(owner=request.user))
		if create_namespace_form.is_valid():
			namespace = create_namespace_form.save()
			return JsonResponse(namespace)
		else:
			return HttpResponse(status=400)
	if request.method != 'GET': return HttpResponseServerError()
	return JsonResponse(Namespace.objects.all())

def namespace(request, name):
	namespace = get_object_or_404(Namespace, name=name)
	if not namespace.can_read(request.user): return HttpResponse(status=403)
	if request.method == 'DELETE':
		if not namespace.can_delete(request.user): return HttpResponse(status=403)
		namespace.delete()
		return HttpResponse()
	if request.method != 'GET': return HttpResponseServerError()
	return JsonResponse(namespace)

def pages(request, name):
	namespace = get_object_or_404(Namespace, name=name)
	if not namespace.can_read(request.user): return HttpResponse(status=403)

	if request.method == 'POST':
		if not namespace.can_update(request.user): return HttpResponse(status=403)
		create_wiki_page_form = CreateWikiPageForm(request.POST, instance=WikiPage(namespace=namespace))
		if create_wiki_page_form.is_valid():
			wiki_page = create_wiki_page_form.save()
			if wiki_page == None: return HttpResponse(status=400)
			return JsonResponse(wiki_page)
		else:
			return HttpResponse(status=400)
	
	if request.method != 'GET': return HttpResponseServerError()
	return JsonResponse(namespace.pages.all())

def page(request, id):
	page = get_object_or_404(WikiPage, pk=id)
	if not page.namespace.can_read(request.user): return HttpResponse(status=403)

	if request.method == 'PUT' or request.method == 'POST':
		if not page.namespace.can_update(request.user): HttpResponse(status=403)
		wiki_page_form = WikiPageForm(request.POST, instance=page)
		if wiki_page_form.is_valid():
			page = wiki_page_form.save()
			return JsonResponse(page)
		else:
			return HttpResponse(status=400)

	if request.method == 'DELETE':
		if not page.namespace.can_update(request.user): HttpResponse(status=403)
		page.delete()
		return HttpResponse(status=200)
	
	if request.method != 'GET': return HttpResponseServerError()
	return JsonResponse(page)

