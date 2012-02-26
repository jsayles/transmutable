import datetime
import traceback
import logging
logger = logging.getLogger(__name__)

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

from api_forms import SearchForm

from discovery import discover_api_forms, discover_search_providers

api_forms = discover_api_forms()
discover_search_providers()

def backbone_js(request):
	return render_to_response('backbone/backbone.js', {'api_forms':api_forms}, context_instance=RequestContext(request), mimetype='application/javascript')

def search(request):
	try:
		if request.method == 'POST':
			search_form = SearchForm(request.POST)
			if search_form.is_valid():
				results = search_form.search(request.user)
				return JsonResponse({'search_results':results})
		return JsonResponse([])
	except:
		logger.exception("Could not search")
		traceback.print_exc()
		
def site(request): return JsonResponse(Site.objects.get_current())
	
def site_serialize_fields(site): return ['domain', 'name']
Site.serialize_fields = site_serialize_fields

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
