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

from models import CompletedItem, CompletedItemRock, Gratitude, WorkDoc
from forms import CompletedItemForm, CompletedItemRockForm, GratitudeForm, WorkDocForm

from transmutable import API, UserResource, UserIsRequestorAuthorization

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

class CompletedItemRockResource(ModelResource):
	completed_item = fields.ForeignKey(CompletedItemResource, 'user')
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		resource_name = 'banana/completed-item-rock'
		queryset = CompletedItemRock.objects.all()
		include_absolute_url = False
		allowed_methods = ['get']
		validation = FormValidation(form_class=CompletedItemRockForm)
		authentication = SessionAuthentication()
		authorization = UserIsRequestorAuthorization()
API.register(CompletedItemRockResource())

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

class WorkDocAuthorization(UserIsRequestorAuthorization):
	def create_detail(self, object_list, bundle):
		'''False because every User always has exactly 1 WorkDoc'''
		return False
	def delete_detail(self, object_list, bundle):
		'''False because every User always has exactly 1 WorkDoc'''
		return False
	def read_list(self, object_list, bundle): 
		'''We don't filter work_docs by user'''
		return object_list

class WorkDocResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	class Meta:
		resource_name = 'banana/work-doc'
		queryset = WorkDoc.objects.all()
		include_absolute_url = True
		allowed_methods = ['get', 'put']
		validation = FormValidation(form_class=WorkDocForm)
		authentication = SessionAuthentication()
		authorization = WorkDocAuthorization()
API.register(WorkDocResource())

# Copyright 2013 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
