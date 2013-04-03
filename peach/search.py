from django.db.models import Q

from models import WikiPage
from transmutable.search import SearchProvider, SearchResult

class ToDoProvider(SearchProvider):
	"""
	Searches the wiki pages for to-do items.
	To-do items look like this: - do something
	"""

	@classmethod
	def display_name(cls): return "To-do"

	@classmethod
	def type_name(cls): return "peach.todo"
	
	def search(self, user, search_terms=[], slice_start=0, slice_end=None):
		terms = search_terms.split()
		if len(terms) == 0: return None
		rough_query = Q(content__contains='\n- ')
		for term in terms: rough_query = rough_query | Q(content__icontains=term)
		results = []			
		for page in WikiPage.objects.filter(namespace__owner=user).filter(rough_query):
			matches = self.todo_matches(terms, page)
			for match in matches:
				results.append((page, match))
			
		if slice_end != None: results = results[slice_start:slice_end]
		return [SearchResult(self, None, result[1], result[0].get_absolute_url()) for result in results]

	def todo_matches(self, terms, wiki_page):
		if not wiki_page.content: return []
		results = []
		for line in wiki_page.content.split('\n'):
			line = line.strip().lower()
			matches = True
			if not line.startswith('- '): continue
			for term in terms:
				if not term in line:
					matches = False
					break
			if matches: results.append(line)
		return results
			
# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
