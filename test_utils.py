from django.test.client import Client
from django.contrib.auth.models import User

def create_user(username, password, first_name=None, last_name=None, email=None, is_staff=False, email_validated=True):
	user = User.objects.create(username=username, is_staff=is_staff, is_superuser=is_staff)
	if first_name: user.first_name = first_name
	if last_name: user.last_name = last_name
	if email: user.email = email
	user.set_password(password)
	user.save()

	profile = user.get_profile()
	profile.email_validated = True
	profile.save()

	client = Client()
	client.login(username=username, password=password)
	return (user, client)
