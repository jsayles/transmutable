import json

from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user, APITestCase

from peach.models import Namespace, WikiPage


import json

from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user, APITestCase

from banana.models import CompletedItem

class APITests(APITestCase):
	namespaces_url = '/api/v0.1/peach/namespace/'
	wiki_pages_url = '/api/v0.1/peach/wiki-page/'

	def setUp(self):
		super(APITests, self).setUp()
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers')
		self.user2, self.client2 = create_user(username='bob', password='1234', first_name='Bob', last_name='Smith')

		self.namespace1 = Namespace.objects.create(name='Joe Biden', owner=self.user1)

	def test_wiki_page(self):
		# Create should work only for logged in users
		data = {
			'name':'Twonk McGee',
			'content':'I only have eyes for you and you and you.',
			'namespace':self.namespace1.get_api_url()
		}
		response = self.api_client.post(APITests.wiki_pages_url, format='json', data=data) # Anonymous
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.post(APITests.wiki_pages_url, format='json', data=data) # Not owner
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		response_json = self.postJSON(APITests.wiki_pages_url, data, self.api_client) # Owner
		self.assertEqual(response_json['namespace'], self.namespace1.get_api_url())
		wiki_page1 = WikiPage.objects.get(pk=response_json['id'])

		# Read
		self.assertTrue(self.namespace1.public)
		self.api_client.client.login(username='alice', password='1234')
		response_json = self.getJSON(wiki_page1.get_api_url(), self.api_client) # Read by owner
		self.api_client.client.login(username='bob', password='1234')
		response_json = self.getJSON(wiki_page1.get_api_url(), self.api_client) # Read by non owner
		self.api_client.client.logout()
		response = self.api_client.get(wiki_page1.get_api_url(), format='json') # API only supports authed users
		self.assertHttpUnauthorized(response)

		# Update
		data['name'] = 'Flink McGoo'
		data['content'] = 'Chuppa chup'
		self.api_client.client.logout()
		response = self.api_client.put(wiki_page1.get_api_url(), format='json', data=data) # Unauth'ed user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.put(wiki_page1.get_api_url(), format='json', data=data) # Non-owner user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		self.putJSON(wiki_page1.get_api_url(), data, self.api_client) # Owner
		response_json = self.getJSON(wiki_page1.get_api_url(), self.api_client)
		self.assertEqual(response_json['name'], data['name'])
		self.assertEqual(response_json['content'], data['content'])

		# Delete
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.delete(wiki_page1.get_api_url(), format='json') # Non-owner user
		self.assertHttpUnauthorized(response)
		self.api_client.client.logout()
		response = self.api_client.delete(wiki_page1.get_api_url(), format='json') # Unauth'ed user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		response = self.api_client.delete(wiki_page1.get_api_url(), format='json') # Owner
		self.assertEqual(response.status_code, 204, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
		response = self.api_client.get(wiki_page1.get_api_url())
		self.assertEqual(response.status_code, 404, 'Response status was %s. Response content: %s' % (response.status_code, response.content))

	def test_namespace(self):

		# Create should work only for logged in users
		data = {
			'display_name':'Tofu I Love'
		}
		response = self.api_client.post(APITests.namespaces_url, format='json', data=data)
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		response_json = self.postJSON(APITests.namespaces_url, data, self.api_client)
		self.assertEqual(response_json['owner'], self.user1.get_api_url())

		# Anyone can read public Namespaces
		self.assertTrue(self.namespace1.public)
		response_json = self.getJSON(self.namespace1.get_api_url(), self.api_client) # Read by owner
		self.api_client.client.login(username='bob', password='1234')
		response_json = self.getJSON(self.namespace1.get_api_url(), self.api_client) # Read by non owner
		self.api_client.client.logout()
		response = self.api_client.get(self.namespace1.get_api_url(), format='json') # API only supports authed users
		self.assertHttpUnauthorized(response)

		# Only the owner can read private Namespaces
		self.namespace1.public = False
		self.namespace1.save()
		self.api_client.client.login(username='alice', password='1234')
		response_json = self.getJSON(self.namespace1.get_api_url(), self.api_client) # Read by owner
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.get(self.namespace1.get_api_url(), format='json') # Read by non-owner
		self.assertHttpUnauthorized(response)
		self.api_client.client.logout()
		response = self.api_client.get(self.namespace1.get_api_url(), format='json') # API only supports authed users
		self.assertHttpUnauthorized(response)

		# Only the owner can update a Namespace
		data = {
			'display_name':'Seitan I Love'
		}
		self.api_client.client.logout()
		response = self.api_client.put(self.namespace1.get_api_url(), format='json', data=data) # Unauth'ed user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.put(self.namespace1.get_api_url(), format='json', data=data) # Non-owner user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		self.putJSON(self.namespace1.get_api_url(), data, self.api_client) # Owner
		response_json = self.getJSON(self.namespace1.get_api_url(), self.api_client)
		self.assertEqual(response_json['display_name'], 'Seitan I Love')

		# Only the owner can delete a Namespace
		self.api_client.client.login(username='bob', password='1234')
		response = self.api_client.delete(self.namespace1.get_api_url(), format='json') # Non-owner user
		self.assertHttpUnauthorized(response)
		self.api_client.client.logout()
		response = self.api_client.delete(self.namespace1.get_api_url(), format='json') # Unauth'ed user
		self.assertHttpUnauthorized(response)
		self.api_client.client.login(username='alice', password='1234')
		response = self.api_client.delete(self.namespace1.get_api_url(), format='json') # Owner
		self.assertEqual(response.status_code, 204, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
		response = self.api_client.get(self.namespace1.get_api_url())
		self.assertEqual(response.status_code, 404, 'Response status was %s. Response content: %s' % (response.status_code, response.content))

