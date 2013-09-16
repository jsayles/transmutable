import markdown
from markdown.inlinepatterns import SimpleTagPattern

PRE_RE = r"(<pre>)(.+?)(</pre>)"

class ElementWhitelistExtension(markdown.extensions.Extension):
	def extendMarkdown(self, md, md_globals):
		"""Modifies inline patterns."""
		md.inlinePatterns.add('pre', SimpleTagPattern(PRE_RE, 'pre'), '<not_strong')

def makeExtension(configs={}):
	return ElementWhitelistExtension(configs=dict(configs))
