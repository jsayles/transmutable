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

class WorkDoc(models.Model):
	"""A markdown document displaying a person's current work queue."""
	user = models.ForeignKey(User, related_name='work_docs', unique=True)
	markup = models.TextField(blank=False, null=False, default='')
	rendered = models.TextField(blank=True, null=True)
	modified = models.DateTimeField(auto_now=True)

	def save_markdown(self, markup):
		self.markup = markup
		self.save()

	def save(self, *args, **kwargs):
		"""When saving the markup, render via markdown and save to self.rendered"""
		self.rendered = markdown(urlize(self.markup))
		super(WorkDoc, self).save(*args, **kwargs)

	def __unicode__(self):
		return 'WordDoc for %s' % self.user
	class Meta:
		ordering = ['user__username']

User.work_doc = property(lambda u: WorkDoc.objects.get_or_create(user=u)[0])
User.get_absolute_url = lambda u: reverse('banana.views.user', kwargs={ 'username':u.username })	
