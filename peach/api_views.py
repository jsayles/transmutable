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

from api_forms import NamespaceForm, CreateNamespaceForm
from models import Namespace

def namespaces(request):
	if request.method == 'POST':
		if not Namespace.can_create(request.user): return HttpResponse(status=403)
		create_namespace_form = CreateNamespaceForm(request.POST, instance=Namespace(owner=request.user))
		if create_namespace_form.is_valid():
			namespace = create_namespace_form.save()
			return JsonResponse(namespace)
		else:
			return HttpResponse(status=400)
	return JsonResponse(Namespace.objects.all())

def namespace(request, name):
	namespace = get_object_or_404(Namespace, name=name)
	if request.method == 'DELETE':
		if not namespace.can_delete(request.user): return HttpResponse(status=403)
		namespace.delete()
		return HttpResponse()
	return JsonResponse(namespace)
