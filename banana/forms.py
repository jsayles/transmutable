from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from models import WorkDoc, CompletedItem

class WorkDocForm(forms.ModelForm):
	class Meta:
		model = WorkDoc
		fields = ('markup',)

class CompletedItemForm(forms.ModelForm):
	markup = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Some awesome thing you did.'}))
	link = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'optional link to promote'}))
	class Meta:
		model = CompletedItem
		fields = ('markup', 'promoted', 'link')

class RockCompletedItemForm(forms.Form):
	completed_item_id = forms.IntegerField()

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
