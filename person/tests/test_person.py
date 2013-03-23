from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse

from person.models import Invite

class BasicViewsTest(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create(username='trevor_smith')
		self.user.set_password('1234')
		self.user.save()
		profile = self.user.get_profile()
		profile.email_validated = True
		profile.save()
		
	def tearDown(self):
		pass

	def test_invites(self):
		num_invites = self.user.get_profile().invites.count()
		Invite.objects.add_invites(3, self.user)
		self.assertEqual(num_invites + 3, self.user.get_profile().invites.count())

	def test_email_validation(self):
		user = User.objects.get(username='trevor_smith')
		profile = user.get_profile()
		self.assertTrue(profile.email_validated)
		url = reverse('person.views.email_validate', kwargs={ 'username':user.username, 'secret':profile.validation_secret() })
		self.failUnlessEqual(self.client.get(url).status_code, 200)
		user = User.objects.get(username='trevor_smith')
		self.assertTrue(user.get_profile().email_validated)
		profile = user.get_profile()
		profile.email_validated = False
		profile.save()
		self.failUnlessEqual(self.client.get(url).status_code, 200)
		user = User.objects.get(username='trevor_smith')
		self.assertTrue(user.get_profile().email_validated)
		

	def test_registration(self):
		self.failIf(self.client.login(username="gronkle_stiltskin", password="98562"))

		self.client = Client()
		self.failUnlessEqual(self.client.get(reverse('person.views.register')).status_code, 200)
		response = self.client.post(reverse('person.views.register'), { 'username':'gronkle_stiltskin', 'password':'98562', 'email':'schlub@wiitoiil.com', 'first_name':'Schlub', 'last_name':'Woot', 'tos':'true' })
		self.failUnlessEqual(response.status_code, 302) # redirected to profile upon successful registration

		self.assertEquals(len(mail.outbox), 1)
		self.assertTrue(mail.outbox[0].subject.endswith(' email validation'))
		
		self.client = Client()
		self.failUnless(self.client.login(username="gronkle_stiltskin", password="98562"))
		
		self.client = Client()
		response = self.client.post(reverse('person.views.register'), { 'username':'gronkle_stiltskin', 'password':'98562', 'email':'schlub2@wiitoiil.com', 'first_name':'Schlub', 'last_name':'Woot', 'tos':'true' })
		self.failUnlessEqual(response.status_code, 200) # should not redirect because the username is a duplicate
		response = self.client.post(reverse('person.views.register'), { 'username':'gronkle_stiltskin2', 'password':'98562', 'email':'schlub@wiitoiil.com', 'first_name':'Schlub', 'last_name':'Woot', 'tos':'true' })
		self.failUnlessEqual(response.status_code, 200) # should not redirect because the email is a duplicate
		response = self.client.post(reverse('person.views.register'), { 'username':'gronkle_stiltskin2', 'password':'98562', 'email':'schlub2@wiitoiil.com', 'first_name':'Schlub', 'last_name':'Woot', })
		self.failUnlessEqual(response.status_code, 200) # should not redirect because the tos is not accepted
		
	def test_basic_views(self):
		public_urls = [
			reverse('person.views.register'),
		]
		private_urls = [
			reverse('person.views.profile', kwargs={ 'username':self.user.username })
		]
		for url in public_urls:
			response = self.client.get(url)
			self.failUnlessEqual(response.status_code, 200, 'failed on url %s: %s' % (url, response.status_code))
		for url in private_urls:
			self.failUnlessEqual(self.client.get(url).status_code, 302, 'failed on url %s' % url)
		self.failUnless(self.client.login(username="trevor_smith", password="1234"))
		for url in private_urls:
			self.failUnlessEqual(self.client.get(url).status_code, 200, 'failed on url %s' % url)
		
