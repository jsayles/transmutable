from api_forms import SearchForm

def search_form(request):
	"""Adds the search form to the common context"""
	return {
		'search_form': SearchForm(),
	}