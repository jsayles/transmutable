from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from models import Namespace, WikiPage

class NamespaceForm(forms.ModelForm):
	
	class Meta:
		model = Namespace

class CreateNamespaceForm(forms.ModelForm):
	class Meta:
		model = Namespace
		fields = ["display_name"]

class WikiPageForm(forms.ModelForm):	
	class Meta:
		model = WikiPage

class CreateWikiPageForm(forms.ModelForm):
	class Meta:
		model = WikiPage
		fields = ["name"]
