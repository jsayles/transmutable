from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.forms.widgets import CheckboxSelectMultiple

import backbone.discovery

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

backbone.discovery.discover_search_providers()
PROVIDER_CHOICES = [(provider.type_name(), provider.display_name()) for provider in backbone.discovery.SEARCH_PROVIDERS]

class SearchForm(forms.Form, APIForm):
	search_terms = forms.CharField()
	search_types = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=PROVIDER_CHOICES)

	def url(self): return reverse('backbone.api_views.search')

	@property
	def selected_providers(self):
		if not self.cleaned_data['search_types']: return backbone.discovery.SEARCH_PROVIDERS
		return [provider for provider in backbone.discovery.SEARCH_PROVIDERS if provider.type_name() in self.cleaned_data['search_types']]

	def search(self):
		results = []
		for provider_class in self.selected_providers:
			provider = provider_class()
			results.extend(provider.search(self.cleaned_data['search_terms']))
		return results
		
class SiteForm(forms.Form, APIForm):
	"""Wraps the Django site object"""
	def url(self): return reverse('backbone.api_views.site')
	class Meta:
		model = Site

