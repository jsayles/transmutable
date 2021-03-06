'''Transmutable is a Django project which provides tools for working in public'''
import os

from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tastypie.api import Api
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication, SessionAuthentication

def file_field_full_path(self): return os.path.join(settings.PROJECT_ROOT, self.path) 
models.fields.files.ImageFieldFile.full_path = property(file_field_full_path)        
models.fields.files.FieldFile.full_path = property(file_field_full_path)

API = Api(api_name='v0.1')

def get_pk_from_detail_url(url):
	if not url: return None
	return url.split('/')[-2]

def get_model_by_resource_url(url, model_class):
	id = get_pk_from_detail_url(url)
	if id == None: return None
	return model_class.objects.get(pk=id)

def get_user_by_resource_url(url):
	'''Returns a User for a resource URL like /api/v0.1/auth/user/3/'''
	return get_model_by_resource_url(url, User)

def serialize_query_set(query_set, resource_class, request):
	'''
	Returns the query_set serialized to JSON
	'resource_class' should be a tastypie Resource and 'request' should be an HttpRequest
	'''
	res = resource_class()
	request_bundle = res.build_bundle(request=request)
	queryset = res.obj_get_list(request_bundle)
	bundles = []
	for obj in query_set:
		bundle = res.build_bundle(obj=obj, request=request)
		bundles.append(res.full_dehydrate(bundle, for_list=True))

	return res.serialize(None, bundles, "application/json")

class UserIsRequestorAuthorization(Authorization):
	'''
	Create: User must be logged in and 'user' must be a resource URL for the logged in user
	Read: Any logged in user can read any resource
	Update: Any logged in user can update their own object
	Delete: Any logged in user can delete their own object
	'''
	def __init__(self, user_field_name='user'):
		self.user_field_name = user_field_name

	def create_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		user = get_user_by_resource_url(bundle.request.POST.get(self.user_field_name, None))
		if user: return bundle.request.user == user
		# self.user_field_name wasn't passed so we'll set it
		bundle.data[self.user_field_name] = reverse('api_dispatch_detail', args=['v0.1', 'auth/user', bundle.request.user.id])
		return True

	def read_detail(self, object_list, bundle):
		return bundle.request.user.is_authenticated()

	def update_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return getattr(bundle.obj, self.user_field_name) == bundle.request.user

	def delete_detail(self, object_list, bundle):
		if not bundle.request.user.is_authenticated(): return False
		return getattr(bundle.obj, self.user_field_name) == bundle.request.user

	def create_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no creates.")

	def read_list(self, object_list, bundle):
		kwargs = {self.user_field_name: bundle.request.user}
		return object_list.filter(**kwargs)

	def update_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no updates.")

	def delete_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no deletes.")

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		include_absolute_url = True
		resource_name = 'auth/user'
		fields = ['username', 'first_name', 'last_name', 'id']
		allowed_methods = ['get']
		filtering = { 'username': ALL }
API.register(UserResource())

from banana.api import CompletedItemResource
from peach.api import NamespaceResource
