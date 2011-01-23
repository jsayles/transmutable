import os
import re
import traceback
import Image
from django.template import Library
from django import template
from django.utils.html import linebreaks
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()

class CompletedItemNode(template.Node):
	def __init__(self):
		self.request = template.Variable('request')
		self.completed_item = template.Variable('completed_item')

	def render(self, context):
		try:
			request = self.request.resolve(context)
			completed_item = self.completed_item.resolve(context)
			return render_to_string('banana/completed_item.frag', {'rocked_it':completed_item.rocked_it(request.user)}, context)
		except template.VariableDoesNotExist:
			print 'does not exist'
			return ''

@register.tag(name="completed_item_widget")
def completed_item_widget(parser, token): return CompletedItemNode()

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
