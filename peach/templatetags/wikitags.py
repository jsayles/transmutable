# Copyright 2009,2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import re
import markdown
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags, linebreaks, urlize

register = template.Library()

@register.filter
def wiki(text):
	"""Convert the text into HTML using markdown and image name replacement."""
	md = markdown.Markdown(safe_mode="escape", extensions=['nofollow', 'whitelist'])
	return md.convert(text)

@register.filter
def include_constants(text):
	from peach.models import WikiConstant
	constants = WikiConstant.objects.all()
	for constant in constants:
		pattern = r'(?:\$%s\$)' % constant.name
		regex = re.compile(r'%s' % pattern)
		text = regex.sub(constant.constant, text)
		# handle the urlized constants which look like %24constant_name%24
		pattern = r'(?:%%24%s%%24)' % constant.name
		regex = re.compile(r'%s' % pattern)
		text = regex.sub(constant.constant, text)
	return text

@register.filter
def truncate(value, arg):
	"""
	Truncates a string after a given number of chars  
	Argument: Number of chars to truncate after
	From: http://www.djangosnippets.org/snippets/163/
	"""
	try:
		length = int(arg)
	except ValueError: # invalid literal for int()
		return value # Fail silently.
	if not isinstance(value, basestring):
		value = str(value)
	if (len(value) > length):
		return value[:length] + "..."
	else:
		return value
