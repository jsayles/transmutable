{% load imagetags %}
{% load wikitags %}

{% block sub-head %}
<script type="text/javascript">
</script>
{% endblock %}

{% if request.user.is_authenticated %}
	<div class="wiki-control-links">
		[<a href="{% url peach.views.wiki_history page.namespace.name page.name %}">page history</a>]
		[<a href="{% url peach.views.wiki_print page.namespace.name page.name %}">print version</a>]
		[<a href="{% url peach.views.wiki_edit page.namespace.name page.name %}">edit this page</a>]
	</div>
{% endif %}

	{% if not hide_title %}<h1><a href="{% url peach.views.index %}">Notes</a> &raquo; <a href="{% url peach.views.namespace page.namespace.name %}">{{ page.namespace.name }}</a> &raquo; {{ page.name }}</h1>{% endif %}

	{% if page.rendered %}
		<div class="rendered-page">{{ page.rendered|include_constants|safe }}</div>
	{% endif %}

	{% if page.wikifile_set.all %}
	<h3>Files:</h3>
	{% endif %}
	{% for file in page.wikifile_set.all %}
		<div class="wiki-file-item">
			<a href="{{ file.file.url }}">{{ file.display_name }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
		</div>
	{% endfor %}
