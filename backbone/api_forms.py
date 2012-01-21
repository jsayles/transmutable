from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

class APIForm(object):
	"""An abstract base class which should be mixed in to resources wrapped by backbone"""

	def url(self):
		"""
		If this resource is only accessable at one URL (with no id) then implement this method and none of the other URL methods.
		"""
		return None

	def collection_url(self):
		"""
		Implement this to indicate where to find a collection of this resource.

		Return a string.
		
		If the collection has an identifier in it, use 1234 and set collection.urlId in JS.
		"""
		return None

	def resource_url(self):
		"""
		Implement this to indicate that the resource URL and the collection URL are different.
		
		Return a string.
		
		Use 1234 as the ID and it will be replaced in JS by model.get('id')
		"""
		return None


	@classmethod
	def form_name(cls):
		name = cls.__name__
		if name.endswith('Form'): return name[0:-4]
		return name

	@classmethod
	def dict(cls): return cls().__dict__

class SearchForm(forms.Form, APIForm):
	search_terms = forms.CharField()
	search_types = forms.CharField(required=False, widget=forms.HiddenInput()) # a space separated list of SearchProvider.type_name strings to search
	excluded_types = forms.CharField(required=False, widget=forms.HiddenInput()) # a space separated list of SearchProvider.type_name string to avoid

	def url(self): return reverse('backbone.api_views.search')

	def search(self):
		from backbone.discovery import SEARCH_PROVIDERS
		results = []
		for provider_class in SEARCH_PROVIDERS:
			provider = provider_class()
			results.extend(provider.search(self.cleaned_data['search_terms']))
		return results
		
class SiteForm(forms.Form, APIForm):
	"""Wraps the Django site object"""
	def url(self): return reverse('backbone.api_views.site')
	class Meta:
		model = Site

