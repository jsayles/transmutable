from django import forms
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from models import *

class ProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('location', 'url', 'bio')

class ProfileSearchForm(forms.Form):
	terms = forms.CharField(required=True)

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo

class InviteRequestForm(forms.ModelForm):
	class Meta:
		model = InviteRequest

class UserCreationForm(forms.ModelForm):
	""" A form that creates a user, with no privileges, from the given username and password. """
	first_name = forms.CharField()
	last_name = forms.CharField()
	username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
	error_message = _("This value must contain only letters, numbers and underscores."))
	email = forms.EmailField(label=_("Email"))
	password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
	tos = forms.BooleanField(label="I accept the terms of service.")

	class Meta:
		model = User
		fields = ("username","email")

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(_("A user with that username already exists."))

	def clean_email(self):
		email = self.cleaned_data["email"]
		if User.objects.filter(email=email).count() > 0:
			raise forms.ValidationError(_("A user with that email already exists."))
		return email

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		if commit:
			user.save()
			profile = user.get_profile()
			profile.save()
		return user

class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'tabindex':'1'}))

class InviteForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'tabindex':'1'}))
	message = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'tabindex':'2'}), required=False)
