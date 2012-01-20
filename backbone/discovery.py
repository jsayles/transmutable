import sys
import types
import traceback

API_FORMS = []

def discover_api_forms():
	"""Find the forms in each app which extend APIForm"""
	from django.conf import settings
	from backbone.api_forms import APIForm
	from django.forms import Form
	from django.forms.models import ModelFormMetaclass
	from django.forms.forms import DeclarativeFieldsMetaclass

	for app_module_name in settings.INSTALLED_APPS:
		try:
			app = __import__(app_module_name)
			__import__('%s.api_forms' % app_module_name)
			app_forms = sys.modules['%s.api_forms' % app_module_name]
		except:
			continue
		for key in dir(app_forms):
			attribute = getattr(app_forms, key)
			if type(attribute) == ModelFormMetaclass or type(attribute) == DeclarativeFieldsMetaclass:
				if not issubclass(attribute, APIForm): continue
				if attribute in API_FORMS: continue
				API_FORMS.append(attribute)
	return API_FORMS

SEARCH_PROVIDERS = []

def discover_search_providers():
	"""Find the classes in each app's search module which extend SearchProvider"""
	from django.conf import settings
	from backbone.search import SearchProvider

	for app_module_name in settings.INSTALLED_APPS:
		try:
			app = __import__(app_module_name)
			__import__('%s.search' % app_module_name)
			search_module = sys.modules['%s.search' % app_module_name]
		except:
			continue
		for key in dir(search_module):
			attribute = getattr(search_module, key)
			try:
				if issubclass(attribute, SearchProvider):
					if attribute == SearchProvider: continue
					if attribute in SEARCH_PROVIDERS: continue
					SEARCH_PROVIDERS.append(attribute)
			except:
				pass
	return SEARCH_PROVIDERS
