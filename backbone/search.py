"""Provides the SearchProvider class which is used by other apps to hook into backbone search."""

from django.db.models import Q
from django.contrib.auth.models import User
from dynamicresponse.emitters import JSONEmitter

class SearchProvider(object):
	"""A base class for all apps to use to provide search results from the common search API"""
	
	@property
	def type_name(self):
		"""
		Should return a string with a unique id for this type of search result.
		For example, if returning to-do's from the apple app, you might return "apple.to-do".
		"""
		raise NotImplementedError()
	
	def search(self, search_terms=[], slice_start=0, slice_end=None):
		"""
		Returns a list of SearchResult instances matching the search_terms.
		search_terms is a list of strings
		"""
		raise NotImplementedError()

class SearchResult(object):
	"""A base class for cross app wrapping of search results"""

	def __init__(self, content=None, source_url=None):
		self._content = content
		self._source_url = source_url
	
	@property
	def content(self):
		"""
		The (non-markeddown) content of the search result
		For example, a to-do result might be "- take out the garbage".
		"""
		return self._content
	
	def source_url(self):
		"""
		The URL to the context from which the result sprang.
		For example, the wiki page from which a to-do search result came.
		"""
		return self._source_url

	def __emittable__(self): return {'content':self.content, 'source_url':self.source_url()}


class UserSearchProvider(SearchProvider):
	"""Searches the user accounts"""
	@property
	def type_name(self): return "backbone.user"
	
	def search(self, search_terms=[], slice_start=0, slice_end=None):
		terms = search_terms.split()
		if len(terms) == 0: return None;
		fname_query = Q(first_name__icontains=terms[0]) 
		lname_query = Q(last_name__icontains=terms[0])
		email_query = Q(email__icontains=terms[0])
		username_query = Q(username__icontains=terms[0])
		for term in terms[1:]:
			fname_query = fname_query | Q(first_name__icontains=term) 
			lname_query = lname_query | Q(last_name__icontains=term) 
			email_query = email_query | Q(email__icontains=term)
			username_query = username_query | Q(username__icontains=term)
		query = User.objects.filter(fname_query | lname_query | email_query | username_query)
		if slice_end != None: query = query[slice_start:slice_end]
		return [SearchResult('%s <%s>' % (user.get_full_name(), user.username), user.get_absolute_url()) for user in query]
