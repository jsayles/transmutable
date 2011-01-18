import os, sys
import time
import csv
import ConfigParser

from django.core.management.base import NoArgsCommand, CommandError
from django.core.files import File
from django.core.management.color import color_style
from django.conf import settings

APP_MEDIA_DIR_NAME = 'app_media'

class Command(NoArgsCommand):
	help = "Soft links everything in <installed_app>/media/ into <project_root>/media/  DOES NOT WORK ON WINDOWS"
	requires_model_validation = False

	def handle_noargs(self, **options):
		for app_name in settings.INSTALLED_APPS: self.link_media_dir(app_name)
			
	def link_media_dir(self, app_module_name):
		app = __import__(app_module_name)
		if '.' in app_module_name: app = sys.modules[app_module_name]
		app_dir = os.path.dirname(app.__file__)

		app_media = os.path.join(app_dir, APP_MEDIA_DIR_NAME)
		if not os.path.exists(app_media): return
		
		for child_name in os.listdir(app_media):
			source = os.path.join(app_media, child_name)
			dest = os.path.join(settings.MEDIA_ROOT, child_name)
			if os.path.exists(dest): continue
			os.symlink(source, dest) # will not work on windows 

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
