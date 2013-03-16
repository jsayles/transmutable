from django.conf import settings
from django.contrib.sites.models import Site

def get_setting(name, default):
	if hasattr(settings, name): return getattr(settings, name)
	return default

def site(request):
	"""Adds site-wide context variables"""
	return {
		'site': Site.objects.get_current(),
		'default_help_url': settings.DEFAULT_HELP_URL,
		'terms_of_service_url': get_setting('TERMS_OF_SERVICE_URL', None),
		'privacy_policy_url': get_setting('PRIVACY_POLICY_URL', None),
		'google_ad_settings': get_setting('GOOGLE_AD_SETTINGS', None),
	}

# Copyright 2010 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
