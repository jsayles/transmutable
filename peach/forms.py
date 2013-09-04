# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import re

from django import forms
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from models import WikiPage, WikiFile, WikiPhoto, Namespace

class ToggleNamespacePublicForm(forms.Form):
	toggle_namespace_public_action = forms.BooleanField(required=True, initial=True, widget=forms.HiddenInput())

class ToggleNamespaceArchiveForm(forms.Form):
	toggle_namespace_archive_action = forms.BooleanField(required=True, initial=True, widget=forms.HiddenInput())

class WikiPhotosForm(forms.Form):
	upload_photos_action = forms.BooleanField(required=True, initial=True, widget=forms.HiddenInput())

	def save(self, wiki_page, request_files):
		results = []
		for name, val  in request_files.items():
			wiki_photo = WikiPhoto(wiki_page=wiki_page)
			wiki_photo.image.save(name, val, save=False)
			wiki_photo.save()
			results.append(wiki_photo)
			if wiki_photo.web_thumb_url == None:
				for photo in results: photo.delete()
				raise IOError('could not read that image')
		return results

class WikiPageForm(forms.ModelForm):
	class Meta:
		model = WikiPage
		fields = ('content',)

class CreateWikiPageForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'create a page'}))
	class Meta:
		model = WikiPage
		fields = ('name',)

class WikiFileForm(forms.ModelForm):
	class Meta:
		model = WikiFile
		fields = ('file','title','description')

class WikiPhotoForm(forms.ModelForm):
	class Meta:
		model = WikiPhoto
		fields = ('image','title','description')

class NamespaceForm(forms.ModelForm):
	display_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'New note name'}))

	class Meta:
		model = Namespace
		fields = ('display_name',)