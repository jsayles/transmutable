import simplejson

from tastypie.test import ResourceTestCase

from django.test import TestCase
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

class APITestCase(ResourceTestCase):

	def getJSON(self, url, client):
		response = client.get(url, format='json')
		self.assertEqual(response.status_code, 200, 'Response status was %s' % response.status_code)
		return simplejson.loads(response.content)

	def postJSON(self, url, data, client): return self.fetchJSON('post', url, data, client)

	def putJSON(self, url, data, client): return self.fetchJSON('put', url, data, client)

	def fetchJSON(self, method, url, data, client):
		response = getattr(client, method)(url, format='json', data=data)

		self.assertTrue(response.status_code >= 200 and response.status_code < 300, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
		if response.status_code == 201:
			response = client.get(response['Location'], format='json')
			self.assertEqual(response.status_code, 200, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
			self.assertValidJSONResponse(response)
			return simplejson.loads(response.content)

		if response.status_code == 204: return None # This happens for PUT and is fine but there is no content JSON to return

		self.assertValidJSONResponse(response)
		return simplejson.loads(response.content)

