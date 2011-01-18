from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User

class SendTestEmailForm(forms.Form):
	email = forms.EmailField(max_length=100, required=True, label="Email *")
	

class CreateAccountForm(forms.Form):
	username = forms.RegexField(max_length=30, regex=r'^[\w.@+-]+$', help_text = "30 characters or fewer. Letters, digits and @/./+/-/_ only.", error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."}, label="Username *")
	first_name = forms.CharField(max_length=100, label="First name *")
	last_name = forms.CharField(max_length=100, label="Last name *")
	email = forms.EmailField(max_length=100, required=True, label="Email *")
	website = forms.URLField(required=False)

	def clean_username(self):
		data = self.cleaned_data['username']
		if User.objects.filter(username=data).count() > 0: raise forms.ValidationError("That username is already in use.")
		return data

	def save(self):
		"Creates the User with the field data and returns the user"
		if not self.is_valid(): raise Exception('The form must be valid in order to save')
		user = User(username=self.cleaned_data['username'], first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], email=self.cleaned_data['email'])
		password = User.objects.make_random_password(length=10)
		user.set_password(password)
		user.save()
		
		profile = user.get_profile()
		profile.website = self.cleaned_data['website']
		profile.email_validated = True
		profile.save()
		print 'Created user:', user.username, user.email
		return (user, password)

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
