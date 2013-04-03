import sys
import types
import traceback

SEARCH_PROVIDERS = []

def discover_search_providers():
	"""Find the classes in each app's search module which extend SearchProvider"""
	from django.conf import settings
	from search import SearchProvider

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

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
