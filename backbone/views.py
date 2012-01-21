import datetime
import traceback

from django.contrib import auth
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from api_forms import SearchForm

@login_required
def search(request):
	if request.method == 'POST':
		search_form = SearchForm(request.POST)
	else:
		search_form = SearchForm()
	return render_to_response('backbone/search.html', { 'search_form':search_form }, context_instance=RequestContext(request))
