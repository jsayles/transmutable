import os
import Image
import urllib
import datetime, calendar
import random
import time
import re
import unicodedata
import traceback
import logging
import pprint
from re import sub

from django.db import models
from django.utils.html import strip_tags,  linebreaks, urlize
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.markup.templatetags.markup import markdown

from person import sanitizeHtml

class MarkedUpModel(models.Model):
	markup = models.TextField(blank=False, null=False, default='')
	rendered = models.TextField(blank=True, null=True)
	modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True, default=datetime.datetime.now())

	def save_markup(self, markup):
		self.markup = markup
		self.save()

	def save(self, *args, **kwargs):
		"""When saving the markup, render via markdown and save to self.rendered"""
		self.rendered = markdown(urlize(sanitizeHtml(self.markup)))
		super(MarkedUpModel, self).save(*args, **kwargs)
	
	class Meta:
		abstract = True
		ordering = ['-created']

class CompletedItemManager(models.Manager):
	def recent(self, max_count=10):
		results = []
		users = {}
		for item in self.all().order_by('-created'):
			if len(results) >= max_count: break
			if users.has_key(item.user.id): continue
			users[item.user.id] = item.user
			results.append(item)
		return results

class CompletedItem(MarkedUpModel):
	"""Something which a user has completed, mostly items taked off of the work doc."""
	user = models.ForeignKey(User, related_name='completed_items')
	objects = CompletedItemManager()
	def flatten(self): return {'user':self.user.username, 'rendered':self.rendered, 'modified':'%s' % self.modified}
	@models.permalink
	def get_absolute_url(self): return ('banana.views.completed_item', [], { 'username':self.user.username, 'id':self.id })
	def __unicode__(self): return 'CompletedItem for %s' % self.user
	
class WorkDoc(MarkedUpModel):
	"""A markdown document displaying a person's current work queue."""
	user = models.ForeignKey(User, related_name='work_docs', unique=True)
	def __unicode__(self):
		return 'WordDoc for %s' % self.user

User.work_doc = property(lambda u: WorkDoc.objects.get_or_create(user=u)[0])
User.get_absolute_url = lambda u: reverse('banana.views.user', kwargs={ 'username':u.username })	

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
