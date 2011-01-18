import os
import time
import urllib
import sys
import random
from datetime import datetime, date, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.sites.models import Site

class Command(BaseCommand):
	help = "Installs the demo data."
	args = "no-reset"
	requires_model_validation = True
	
	def handle(self, *labels, **options):
		from banana.models import WorkDoc, CompletedItem
		if 'no-reset' not in labels:
			call_command('syncdb', interactive=False)
			call_command('migrate', interactive=False)
			call_command('reset', 'peach', interactive=False)
			call_command('reset', 'banana', interactive=False)
			#for user in User.objects.all(): user.delete()
			
		site = Site.objects.get_current()
		site.domain = '127.0.0.1:8000'
		site.name = 'Transmutable Work'
		site.save()
				
		person1 = self.create_user('trevor', '1234', 'Trevor F.', 'Smith', 'Seattle, WA', is_staff=True, is_superuser=True)
		person1.work_doc.save_markup("""#Thursday:
* Legal homework
* Call Dr. Foolish
* read [the NYT](http://nytimes.com/ "NY Times")

#Wednesday:
1. Figure out mortgage insurance screwup
1. Baby aspirin

#To queue:

* Figure out and pay overdue 2038 taxes
* Write Jerry
* Watch The Joy of Stats: http://www.gapminder.org/videos/the-joy-of-stats/
* Get a new driver's license, update ZipCar

Read "Good to Great"
""")
		completed_item1 = self.create_completed_item(person1, "Launched http://transmutable.com/")
		completed_item2 = self.create_completed_item(person1, """Completed \"For the Win\"

I really wanted the kids to learn:

* grass roots organization
* dumpling recipes
* cross generation hair styles""")
		completed_item3 = self.create_completed_item(person1, "Submitted bid to Cthulu")
		completed_item4 = self.create_completed_item(person1, "Rebooted the Internet")
		
		person2 = self.create_user('jerry', '1234', 'Jerry', 'Dorfendorf', 'Detroit, MI', is_staff=False, is_superuser=False)
		person2.work_doc.save_markup("I am currently flying between one of three coasts.")
		completed_item5 = self.create_completed_item(person2, "Joined Two Pieces Of Wood")
		
		person3 = self.create_user('amy', '1234', 'Amy', 'Scout', 'Bothell, WA', is_staff=False, is_superuser=False)
		
		namespace1 = self.create_namespace('Dev Notes', person1)
		page1 = self.create_wiki_page(namespace1, 'SplashPage', """#This is the SplashPage
* this is a list item
* and another item
* you think there's more, right?
* well, you are correct.

[This link](http://example.net/) has no title attribute.
""")

		namespace2 = self.create_namespace('Dog Walks in Bothell', person3)
		page2 = self.create_wiki_page(namespace2, 'How to Make Dog Biscuits', """Google the recipe. CamelCase """)
	
	def create_wiki_page(self, namespace, name, content):
		from peach.models import WikiPage
		return WikiPage.objects.create(namespace=namespace, name=name, content=content)
	
	def create_namespace(self, name, owner):
		from peach.models import Namespace
		return Namespace.objects.get_or_create(display_name=name, owner=owner)[0]

	def create_completed_item(self, user, markup):
		from banana.models import CompletedItem
		return CompletedItem.objects.create(user=user, markup=markup)
	
	def create_user(self, username, password, first_name=None, last_name=None, location=None, is_staff=False, is_superuser=False):
		person, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, is_staff=is_staff, is_superuser=is_superuser)
		person.set_password(password)
		person.save()
		return person

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
