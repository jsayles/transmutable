import traceback
import logging
logger = logging.getLogger(__name__)

from search_forms import SearchForm
from dynamicresponse.json_response import JsonResponse

def search(request):
	try:
		if request.method == 'POST':
			search_form = SearchForm(request.POST)
			if search_form.is_valid():
				results = search_form.search(request.user)
				return JsonResponse({'search_results':results})
		return JsonResponse([])
	except:
		logger.exception("Could not search")
		traceback.print_exc()
