from django.contrib.sites.models import Site
from django.conf import settings

def pagination(request):
	"""
	Inserts a variable representing the current page onto the request object if
	it exists in either **GET** or **POST** portions of the request.
	"""
	try:
		request.page = int(request.REQUEST['page'])
	except (KeyError, ValueError):
		request.page = 1
	return { }

def person_context(request):
	"""Adds a context variables related to accounts, registration, and invites"""
	return {
		'open_registration':settings.OPEN_REGISTRATION, 
		'open_invite':settings.OPEN_INVITE, 
		'open_invite_request':settings.OPEN_INVITE_REQUEST
	}
