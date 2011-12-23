from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from models import Namespace
from backbone.api_forms import APIForm

class NamespaceForm(forms.ModelForm, APIForm):
	def url_id_field(self): return "name"
	def collection_url(self): return reverse('peach.api_views.namespaces')
	def resource_url(self): return reverse('peach.api_views.namespace', kwargs={'name':'1234'})
	
	class Meta:
		model = Namespace

class CreateNamespaceForm(forms.ModelForm):
	class Meta:
		model = Namespace
		fields = ["display_name"]
