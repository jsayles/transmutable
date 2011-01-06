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
		from banana.models import WorkDoc
		if 'no-reset' not in labels:
			call_command('syncdb', interactive=False)
			call_command('migrate', interactive=False)
			call_command('reset', 'banana', interactive=False)
			for user in User.objects.all(): user.delete()
			
		site = Site.objects.get_current()
		site.domain = '127.0.0.1:8000'
		site.name = 'Transmutable'
		site.save()
		
		person1 = self.create_user('trevor', '1234', 'Trevor F.', 'Smith', 'Seattle, WA', is_staff=True, is_superuser=True)
		person2 = self.create_user('jerry', '1234', 'Jerry', 'Dorfendorf', 'Detroit, MI', is_staff=False, is_superuser=False)
		
		workdoc1 = person1.work_doc
		workdoc1.markup = """1. First Item
2. Second Item
"""
		workdoc1.save()
		
	def create_user(self, username, password, first_name=None, last_name=None, location=None, is_staff=False, is_superuser=False):
		person, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, is_staff=is_staff, is_superuser=is_superuser)
		person.set_password(password)
		person.save()
		return person

# Copyright 2010 by Trevor F. Smith. All Rights Reserved.