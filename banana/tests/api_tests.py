import json

from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user, APITestCase

from banana.models import CompletedItem

class APITests(APITestCase):
	completed_items_url = '/api/v0.1/banana/completed-item/'

	def setUp(self):
		super(APITests, self).setUp()
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers')
		self.user2, self.client2 = create_user(username='bob', password='1234', first_name='Bob', last_name='Smith')

	def test_completed_items(self):
		self.api_client.client.login(username='alice', password='1234')
		user1_json = self.getJSON('/api/v0.1/auth/user/%i/' % self.user1.id, self.api_client)
		user2_json = self.getJSON('/api/v0.1/auth/user/%i/' % self.user2.id, self.api_client)
		self.api_client.client.logout()

		self.assertHttpUnauthorized(self.api_client.get(APITests.completed_items_url, format='json'))
		data = {
			'markup':'I did a thing',
			'user':user1_json['resource_uri']
		}
		response = self.api_client.post(APITests.completed_items_url, format='json', data=data)
		self.assertHttpUnauthorized(response)

		self.api_client.client.login(username='alice', password='1234')

		response = self.api_client.get(APITests.completed_items_url, format='json')
		self.assertValidJSONResponse(response)

		self.api_client.client.logout()
		response = self.api_client.get(APITests.completed_items_url, format='json')
		self.assertHttpUnauthorized(response)

		self.api_client.client.login(username='alice', password='1234')
		response_json = self.getJSON(APITests.completed_items_url, self.api_client)
		self.assertEqual(len(response_json['objects']), 0)

		# Create
		response_json = self.postJSON(APITests.completed_items_url, data, self.api_client)
		# Read
		response = self.api_client.get(response_json['resource_uri'], format='json')
		self.assertValidJSONResponse(response)
		# Update
		self.putJSON(response_json['resource_uri'], {'markup':'Knock it off'}, self.api_client)
		new_response_json = self.getJSON(response_json['resource_uri'], self.api_client)
		self.assertEqual(new_response_json['markup'], 'Knock it off')
		# Delete
		response = self.api_client.delete(response_json['resource_uri'])
		self.assertEqual(response.status_code, 204, 'Response status was %s. Response content: %s' % (response.status_code, response.content))
		response = self.api_client.get(response_json['resource_uri'])
		self.assertEqual(response.status_code, 404, 'Response status was %s. Response content: %s' % (response.status_code, response.content))

		# Check that users can't post as someone else
		data['user'] = user2_json['resource_uri']
		response = self.api_client.post(APITests.completed_items_url, format='json', data=data)
		self.assertHttpUnauthorized(response)

