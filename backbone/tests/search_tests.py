
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user

class SearchTests(TestCase):
	
	def setUp(self):
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers')
		
	def tearDown(self):
		pass

	def test_user_search(self):
		response = self.client1.get(reverse('backbone.views.search'))
		self.failUnlessEqual(response.status_code, 200)
		response = self.client1.post(reverse('backbone.views.search'), {'search_terms':'alice'})
		self.failUnlessEqual(response.status_code, 200)
