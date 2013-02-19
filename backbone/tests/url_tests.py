from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user, APITestCase

from backbone.url_resource import generate_url_resource

class URLTests(APITestCase):
	
	def setUp(self):
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers')
		
	def tearDown(self):
		pass

	def test_resource(self):
		resource = generate_url_resource()
		self.assertTrue(len(resource['resolvers']) > 0)
		self.assertTrue(len(resource['patterns']) > 0)
		json = self.getJSON(reverse('backbone.views.urls'), self.client1)
		self.assertEqual(len(resource['resolvers']), len(json['resolvers']))
		self.assertEqual(len(resource['patterns']), len(json['patterns']))
