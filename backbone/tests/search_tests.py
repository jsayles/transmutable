
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from transmutable.test_utils import create_user
from backbone.api_forms import SearchForm

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

		search_data = {'search_terms':"alice"}
		search_form = SearchForm(search_data)
		self.assertTrue(self.user1, search_form.is_valid())
		results = search_form.search(self.user1)
		self.assertEqual(len(results), 1)

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
