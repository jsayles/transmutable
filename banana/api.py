from datetime import datetime, timedelta, date

from tastypie import fields
from tastypie.api import Api
from tastypie.paginator import Paginator
from tastypie.exceptions import Unauthorized
from tastypie.validation import FormValidation
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from models import CompletedItem, Gratitude
from forms import CompletedItemForm, GratitudeForm

from transmutable import API

class UserIsRequestorAuthorization(Authorization):
	'''
	Create: User must be logged in and 'user' must be a resource URL for the logged in user
	Read: Any logged in user can read any resource
	Update: Any logged in user can update their own object
	Delete: Any logged in user can delete their own object
	'''
	def get_user_by_resource_url(self, url):
		if not url: return None
		user_id = url.split('/')[-2]
		return User.objects.get(pk=user_id)

	def create_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		user = self.get_user_by_resource_url(bundle.request.POST.get('user', None))
		if user: return bundle.request.user == user
		# 'user' wasn't passed so we'll set it
		bundle.data['user'] = reverse('api_dispatch_detail', args=['v0.1', 'auth/user', bundle.request.user.id])
		return True

	def read_detail(self, object_list, bundle):
		return bundle.request.user.is_authenticated()

	def update_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return bundle.obj.user == bundle.request.user

	def delete_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return bundle.obj.user == bundle.request.user

	def create_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no creates.")

	def read_list(self, object_list, bundle):
		return object_list.filter(user=bundle.request.user)

	def update_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no updates.")

	def delete_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no deletes.")

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'auth/user'
		fields = ['username', 'first_name', 'last_name', 'id']
		allowed_methods = ['get']
		filtering = { 'username': ALL }
API.register(UserResource())

class CompletedItemResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		resource_name = 'banana/completed-item'
		queryset = CompletedItem.objects.all()
		include_absolute_url = True
		allowed_methods = ['get', 'post', 'put', 'delete']
		validation = FormValidation(form_class=CompletedItemForm)
		authentication = SessionAuthentication()
		authorization = UserIsRequestorAuthorization()
API.register(CompletedItemResource())

class GratitudeResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		resource_name = 'banana/gratitude'
		queryset = Gratitude.objects.all()
		include_absolute_url = True
		allowed_methods = ['get', 'post', 'put', 'delete']
		validation = FormValidation(form_class=GratitudeForm)
		authentication = SessionAuthentication()
		authorization = UserIsRequestorAuthorization()
API.register(GratitudeResource())

# Copyright 2013 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
