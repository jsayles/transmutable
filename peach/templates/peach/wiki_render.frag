{% load imagetags %}
{% load wikitags %}

{% block sub-head %}
<script>
$(document).ready(function() {
	{% if is_mobile %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.mobile_views.wiki_edit page.namespace.name page.name %}";
		});
	{% else %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_edit page.namespace.name page.name %}";
		});
		$('button[name="print-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_print page.namespace.name page.name %}";
		});
		$('button[name="history-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_history page.namespace.name page.name %}";
		});
	{% endif %}
});
</script>
{% endblock %}

{% if request.user.is_authenticated and page.namespace.owner.username == request.user.username %}
	<div class="wiki-control-links">
	{% if not is_mobile %}
		<button name="history-button">history</button>
		<button name="print-button">print</button>
	{% endif %}
	<button name="edit-button" class="positive">edit</button>
	</div> 
{% endif %}

	{% if not hide_title %}<h1><a href="{% url peach.views.namespace page.namespace.name %}">{{ page.namespace.display_name }}</a> &raquo; {{ page.name }}:</h1>{% endif %}

	{% if page.rendered %}
		<div class="rendered-wrapper">{{ page.rendered|include_constants|safe }}</div>
	{% endif %}

	{% if page.wikifile_set.all %}
	<h3>Files:</h3>
	{% endif %}
	{% for file in page.wikifile_set.all %}
		<div class="wiki-file-item">
			<a href="{{ file.file.url }}">{{ file.display_name }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
		</div>
	{% endfor %}
