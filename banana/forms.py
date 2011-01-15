from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from models import WorkDoc, CompletedItem

class WorkDocForm(forms.ModelForm):
	class Meta:
		model = WorkDoc
		fields = ('markup',)

class CompletedItemForm(forms.ModelForm):
	markup = forms.TextInput()
	class Meta:
		model = CompletedItem
		fields = ('markup',)