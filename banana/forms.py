from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from models import WorkDoc

class WorkDocForm(forms.ModelForm):
	class Meta:
		model = WorkDoc
		fields = ('markup',)
