from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from backbone.api_forms import APIForm

from models import Namespace, WikiPage

class NamespaceForm(forms.ModelForm, APIForm):
	def collection_url(self): return reverse('peach.api_views.namespaces')
	def resource_url(self): return reverse('peach.api_views.namespace', kwargs={'id':'1234'})
	
	class Meta:
		model = Namespace

class CreateNamespaceForm(forms.ModelForm):
	class Meta:
		model = Namespace
		fields = ["display_name"]

class WikiPageForm(forms.ModelForm, APIForm):
	def collection_url(self): return reverse('peach.api_views.pages', kwargs={'id':'1234'})
	def resource_url(self): return reverse('peach.api_views.page', kwargs={'id':1234})
	
	class Meta:
		model = WikiPage

class CreateWikiPageForm(forms.ModelForm):
	class Meta:
		model = WikiPage
		fields = ["name"]
