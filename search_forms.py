from django import forms

from django.forms.widgets import CheckboxSelectMultiple

import discovery

discovery.discover_search_providers()
PROVIDER_CHOICES = [(provider.type_name(), provider.display_name()) for provider in discovery.SEARCH_PROVIDERS]

class SearchForm(forms.Form):
	search_terms = forms.CharField()
	search_types = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=PROVIDER_CHOICES)

	def url(self): return reverse('search_views.search')

	@property
	def selected_providers(self):
		if not self.cleaned_data['search_types']: return discovery.SEARCH_PROVIDERS
		return [provider for provider in discovery.SEARCH_PROVIDERS if provider.type_name() in self.cleaned_data['search_types']]

	def search(self, user):
		results = []
		for provider_class in self.selected_providers:
			provider = provider_class()
			results.extend(provider.search(user, self.cleaned_data['search_terms']))
		return results
