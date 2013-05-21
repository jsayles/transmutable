import datetime
import pprint
import urllib
import logging 
import calendar
import tempfile
import traceback
from time import time

from django.db.models import Q
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Context, loader
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import django.contrib.contenttypes.models as content_type_models
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.middleware.csrf import _get_new_csrf_key 
from models import *
from forms import *

from uploadhandlers import QuotaUploadHandler

def index(request):
	return render_to_response('person/index.html', { }, context_instance=RequestContext(request))

@login_required
def find_people(request):
	profile_search_results = None
	if request.method == 'POST':
		profile_search_form = ProfileSearchForm(request.POST)
		if profile_search_form.is_valid():
			profile_search_results = UserProfile.objects.search(profile_search_form.cleaned_data['terms'])
	else:
		profile_search_form = ProfileSearchForm()
	return render_to_response('person/find_people.html', { 'profile_search_form':profile_search_form, 'profile_search_results':profile_search_results }, context_instance=RequestContext(request))

@login_required
def profile_redirect(request):
	return HttpResponseRedirect(request.user.get_profile().get_absolute_url())

def register(request):
	if request.method == 'POST':
		registration_form = UserCreationForm(request.POST)
		if registration_form.is_valid():
			user = registration_form.save()
			user.backend='django.contrib.auth.backends.ModelBackend' #TODO figure out what is the right thing to do here
			auth.login(request, user)
			user.get_profile().send_email_validation()
			return HttpResponseRedirect(reverse('banana.views.user', kwargs={'username':user.username}))
	else:
		registration_form = UserCreationForm()
	return render_to_response('person/register.html', { 'registration_form':registration_form }, context_instance=RequestContext(request))

def invite(request, secret):
	invite = get_object_or_404(Invite, secret=secret)
	if request.method == 'POST':
		registration_form = UserCreationForm(request.POST)
		if invite.used_by == None and registration_form.is_valid():
			user = registration_form.save()
			user.backend='django.contrib.auth.backends.ModelBackend' #TODO figure out what is the right thing to do here
			auth.login(request, user)
			invite.used_by = user
			invite.save()
			response = HttpResponseRedirect(reverse('banana.views.user', kwargs={'username':user.username}))
			# This is nasty but necessary because otherwise the session has no csrf cookie and thus cannot POST, which makes for a really bad user experience.
			if not "CSRF_COOKIE" in request.META:
				request.META["CSRF_COOKIE"] = _get_new_csrf_key()
				print 'Set new csrf cookie', request.META['CSRF_COOKIE']
				response.set_cookie(settings.CSRF_COOKIE_NAME,
									request.META["CSRF_COOKIE"],
									max_age = 60 * 60 * 24 * 7 * 52,
									domain=settings.CSRF_COOKIE_DOMAIN,
									path=settings.CSRF_COOKIE_PATH,
									secure=settings.CSRF_COOKIE_SECURE
									)
			return response
	else:
		registration_form = UserCreationForm()
	return render_to_response('person/invite.html', { 'registration_form':registration_form, 'invite':invite }, context_instance=RequestContext(request))

@login_required
def invites(request):
	message = None
	if request.method == 'POST':
		invite_form = InviteForm(request.POST)
		if invite_form.is_valid():
			invites = request.user.get_profile().available_invites()
			if len(invites) == 0:
				message = 'Whoops, you have no free invites.'
			else:
				invite = invites[0]
				site = Site.objects.get_current()
				message = render_to_string('person/email/invite.txt', { 'site':site, 'message':strip_tags(invite_form.cleaned_data['message']), 'invite':invite, 'inviter':request.user.get_profile() })
				subject = '%s invites you to %s' % (request.user.get_full_name(), site.name)
				send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [invite_form.cleaned_data['email']], fail_silently=False)
				invite.sent_to = invite_form.cleaned_data['email']
				invite.available = False
				invite.save()
				message = 'Your invite is on its way!'
				invite_form = InviteForm()
	else:
		invite_form = InviteForm()
	return render_to_response('person/invites.html', { 'message':message, 'invite_form':invite_form }, context_instance=RequestContext(request))

@login_required
def photo_edit(request):
	profile = request.user.get_profile()
	if request.method == 'POST':
		photo_form = PhotoForm(request.POST, request.FILES)
		if photo_form.is_valid():
			try:
				photo = photo_form.save()
				if profile.photo: profile.photo.delete()
				profile.photo = photo 
				profile.save()
			except:
				traceback.print_exc()
				logging.exception('Could not upload the image')
	return HttpResponseRedirect('%s#edit-photo' % reverse('person.views.profile', kwargs={'username':request.user.username}))

@login_required
def password_edit(request):
	#request.upload_handlers.insert(0, QuotaUploadHandler())
	profile = request.user.get_profile()
	if request.method == 'POST':
		password_change_form = PasswordChangeForm(profile.user, request.POST)
		if password_change_form.is_valid():
			password_change_form.save()
			password_change_form = PasswordChangeForm(profile.user)
			message = 'Your password has been changed.'
		else:
			message = 'Your password has not been changed.'
	else:
		message = 'Your password has not been changed'
	
	return HttpResponseRedirect('%s#change-password?message=%s' % (reverse('person.views.profile', kwargs={'username':request.user.username}), message))


@login_required
def profile(request, username):
	user = get_object_or_404(User, username=username)
	profile = user.get_profile()
	message = None
	if request.method == 'POST' and request.user.is_authenticated() and request.user.id == profile.user.id:
		profile_form = ProfileForm(request.POST, instance=profile)
		if profile_form.is_valid():
			profile_form.save()
			profile = get_object_or_404(UserProfile, user__username=request.user.username)
			profile_form = ProfileForm(instance=profile)
			message = "Your profile has been saved."
	else:
		profile_form = ProfileForm(instance=profile)
	return render_to_response('person/profile.html', { 'profile':profile, 'password_change_form':PasswordChangeForm(profile.user), 'profile_form':profile_form, 'photo_form':PhotoForm(instance = profile.photo or None), 'message':message }, context_instance=RequestContext(request))

def email_validate(request, username, secret):
	user = get_object_or_404(User, username=username)
	profile = user.get_profile()
	if profile.email_validated:
		message = 'That email address has been validated. Thanks!'
	elif profile.validation_secret() == secret:
		profile.email_validated = True
		profile.save()
		message = 'That email address is now validated. Thanks!'
	else:
		message = 'Sorry, we could not validate that email address.  Has it changed since this link was requested?'
	return render_to_response('person/email_validate.html', { 'user':user, 'message':message }, context_instance=RequestContext(request))
	
def password_reset(request):
	error_message = None
	wait_for_it = None
	if request.method == "GET" and request.GET.has_key(PASSWORD_RESET_SECRET_PARAMETER) and request.GET.has_key(PASSWORD_RESET_ID_PARAMETER):
		password_reset_form = PasswordResetForm()
		try:
			user = User.objects.get(pk=request.GET[PASSWORD_RESET_ID_PARAMETER])
			if not user.is_active:
				error_message = "That account is unavailable."
			elif user.password.split("$")[2] != request.GET[PASSWORD_RESET_SECRET_PARAMETER]:
				error_message = "That account has a different secret.  Perhaps this reset link has expired or has been used already?"
			else:
				password = User.objects.make_random_password()
				user.set_password(password)
				user.save()
				return render_to_response('person/password_reset.html', {'error_message': None, 'new_password': password }, context_instance=RequestContext(request))
		except:
			logging.debug("Could not find account: %s", pprint.pformat(traceback.format_exc()))
			error_message = "That account could not be found."
	elif request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			try:
				user = User.objects.get(email=password_reset_form.cleaned_data['email'])
				if not user.is_active or user.password == None or len(user.password.split("$")) < 3:
					error_message = "That account is unavailable."
				else:
					secret = user.password.split("$")[2]
					url_path = reverse('person.views.password_reset', kwargs={ })
					reset_url = "http://%s%s?%s=%s&%s=%s" % (Site.objects.get_current().domain, url_path, PASSWORD_RESET_SECRET_PARAMETER, secret, PASSWORD_RESET_ID_PARAMETER, user.id)
					message = render_to_string('person/email/password_reset_email.txt', { 'user': user, 'reset_url': reset_url })
					user.email_user("Password Reset", message, settings.DEFAULT_FROM_EMAIL)
					wait_for_it = True
					logging.debug("Sent password reset to %s", user.username)
			except:
				traceback.print_exc()
				logging.debug("Error generating a password reset: %s", pprint.pformat(traceback.format_exc()))
				error_message = "There was an error resetting that account."
	else:
		password_reset_form = PasswordResetForm()
	return render_to_response('person/password_reset.html', {'wait_for_it': wait_for_it, 'error_message': error_message, 'password_reset_form': password_reset_form }, context_instance=RequestContext(request))
