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

from models import Namespace, WikiPage
from forms import NamespaceForm, WikiPageForm

from transmutable import API, UserResource, UserIsRequestorAuthorization
from transmutable import get_user_by_resource_url, get_pk_from_detail_url, get_model_by_resource_url

class NamespaceAuthorization(UserIsRequestorAuthorization):
	def read_detail(self, object_list, bundle):
		'''Anyone can read Namespace if public == True, otherwise only the owner can read it'''
		if not bundle.request.user.is_authenticated(): return False
		if bundle.obj.public: return True
		return bundle.request.user == bundle.obj.owner

class NamespaceResource(ModelResource):
	owner = fields.ForeignKey(UserResource, 'owner')
	class Meta:
		queryset = Namespace.objects.all()
		resource_name = 'peach/namespace'
		fields = ['name', 'display_name', 'public', 'archive']
		allowed_methods = ['get', 'put', 'post', 'delete']
		validation = FormValidation(form_class=NamespaceForm)
		authentication = SessionAuthentication()
		authorization = NamespaceAuthorization(user_field_name='owner')
API.register(NamespaceResource())

def get_namespace_by_resource_url(url):
	'''Returns a Namespace for a resource URL like /api/v0.1/peach/namespace/3/'''
	return get_model_by_resource_url(url, Namespace)

class WikiPageAuthorization(Authorization):
	'''
	Create: User must be logged in and 'namespace' must be a resource URL for a Namespace owned by the logged in user
	Read: If the WikiPage's Namespace is public, True.  Otherwise, only if owned by the logged in user
	Update: Any logged in user can update their own object
	Delete: Any logged in user can delete their own object
	'''

	def create_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		if not 'namespace' in bundle.data: return False
		namespace = get_namespace_by_resource_url(bundle.data['namespace'])
		if not namespace: return False
		if namespace.owner != bundle.request.user: return False
		return True

	def read_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		if bundle.obj.namespace.public == True: return True
		return bundle.obj.namespace.owner == bundle.request.user

	def update_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return bundle.obj.namespace.owner == bundle.request.user

	def delete_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return bundle.obj.namespace.owner == bundle.request.user

	def create_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no creates.")

	def read_list(self, object_list, bundle):
		return object_list.filter(namespace__owner=bundle.request.user)

	def update_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no updates.")

	def delete_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no deletes.")


class WikiPageResource(ModelResource):
	namespace = fields.ForeignKey(NamespaceResource, 'namespace')
	class Meta:
		queryset = WikiPage.objects.all()
		resource_name = 'peach/wiki-page'
		allowed_methods = ['get', 'post', 'put', 'delete']
		validation = FormValidation(form_class=WikiPageForm)
		authentication = SessionAuthentication()
		authorization = WikiPageAuthorization()
API.register(WikiPageResource())

# Copyright 2013 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
