import json

from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user, APITestCase

from peach.models import Namespace, WikiPage

class APITests(APITestCase):
	
	def setUp(self):
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers')
		self.namespace1 = Namespace.objects.create(name='Joe Biden', owner=self.user1)

	def tearDown(self):
		pass

	def test_basics(self):
		data = {
			'display_name':'Obama'
		}		
		response = self.client1.post(reverse('peach.api_views.namespaces'), data)
		self.failUnlessEqual(response.status_code, 200)
		self.assertEqual(1, Namespace.objects.filter(owner=self.user1, display_name=data['display_name']).count())
		json_response = json.loads(response.content)
		namespace2 = Namespace.objects.get(id=json_response['id'])

		page2 = WikiPage.objects.create(namespace=namespace2, name='White House')
		response = self.client1.delete(reverse('peach.api_views.page', kwargs={'id':page2.id}))
		self.failUnlessEqual(response.status_code, 200)

		page3 = WikiPage.objects.create(namespace=namespace2, name='Chicago House')

		response = self.client1.delete(reverse('peach.api_views.namespace', kwargs={'id':namespace2.id}))
		self.failUnlessEqual(response.status_code, 200)
		self.assertEqual(0, Namespace.objects.filter(id=namespace2.id).count())
		self.assertEqual(0, WikiPage.objects.filter(id=page3.id).count())



