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

from peach.templatetags.wikitags import wiki

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
		self.rendered = wiki(self.markup)
		super(MarkedUpModel, self).save(*args, **kwargs)
	
	class Meta:
		abstract = True
		ordering = ['-created']

class Gratitude(MarkedUpModel):
	"""Something for which we are grateful"""
	user = models.ForeignKey(User, related_name='gratitudes')

	def flatten(self): return {
		'id':self.id,
		'user':self.user.username, 
		'markup':self.markup, 
		'rendered':self.rendered, 
		'modified':'%s' % self.modified,
		'created':'%s' % self.created
	}

	@staticmethod
	def can_create(user): return user.is_authenticated()
	def can_read(self, user): return True
	def can_update(self, user): return self.user == user
	def can_delete(self, user): return self.user == user

	@models.permalink
	def get_absolute_url(self): return ('banana.views.gratitude', [], { 'id':self.id })

class CompletedItemManager(models.Manager):
	def recent(self, max_count=10, created_after=None, exclude_users_younger_than=None):
		results = []
		users = {}
		if created_after:
			items = self.filter(created__gte=created_after)
		else:
			items = self.all()

		for item in items.order_by('-created').select_related():
			if len(results) >= max_count: break
			if users.has_key(item.user.id): continue 
			if item.user.get_profile().mute: continue
			if exclude_users_younger_than and item.user.date_joined > exclude_users_younger_than: continue
			users[item.user.id] = item.user
			results.append(item)
		return results

class CompletedItem(MarkedUpModel):
	"""Something which a user has completed, mostly items taked off of the work doc."""
	user = models.ForeignKey(User, related_name='completed_items')

	# These are used by promoted links (aka ta-da's)
	promoted = models.BooleanField(default=False, blank=False, null=False)
	link = models.URLField(verify_exists=False, max_length=1000, blank=True, null=True)
	
	objects = CompletedItemManager()
	def flatten(self): return {'id':self.id, 'user':self.user.username, 'promoted':self.promoted, 'link':self.link, 'rendered':self.rendered, 'modified':'%s' % self.modified, 'created':'%s' % self.created, 'rock_count':self.rock_count}

	@staticmethod
	def can_create(user): return user.is_authenticated()
	def can_read(self, user): return True
	def can_update(self, user): return self.user == user
	def can_delete(self, user): return self.user == user
	
	def rocked_it(self, user):
		if not user.is_authenticated(): return False
		return CompletedItemRock.objects.filter(completed_item=self, user=user).count() == 1

	@property
	def rock_count(self): return CompletedItemRock.objects.filter(completed_item=self).count()
	
	@models.permalink
	def get_absolute_url(self): return ('banana.views.completed_item', [], { 'id':self.id })
	def __unicode__(self): return 'CompletedItem for %s' % self.user

class CompletedItemRock(models.Model):
	"""Indicates that someone other than the completed item owner thinks that the completed item rocks."""
	completed_item = models.ForeignKey(CompletedItem, blank=False, null=False, related_name='rocks')
	user = models.ForeignKey(User, blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)
	def flatten(self): return {'user':self.user.username, 'completed_item':self.completed_item.flatten(), 'created':'%s' % self.created}

class WorkDoc(MarkedUpModel):
	"""A markdown document displaying a person's current work queue."""
	user = models.ForeignKey(User, related_name='work_docs', unique=True)

	@staticmethod
	def can_create(user): return user.is_authenticated()
	def can_read(self, user): return True
	def can_update(self, user): return self.user == user
	def can_delete(self, user): return self.user == user
	
	def flatten(self): return {'user':self.user.username, 'markup':self.markup, 'rendered':self.rendered, 'modified':'%s' % self.modified}
	def __unicode__(self):
		return 'WordDoc for %s' % self.user

User.work_doc = property(lambda u: WorkDoc.objects.get_or_create(user=u)[0])
User.get_absolute_url = lambda u: reverse('banana.views.user', kwargs={ 'username':u.username })	
User.has_unused_tada = lambda u: u.date_joined < datetime.datetime.now() - datetime.timedelta(days=2) and CompletedItem.objects.filter(user=u).filter(promoted=True).filter(created__gt=datetime.datetime.now() - datetime.timedelta(days=2)).count() == 0
# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
