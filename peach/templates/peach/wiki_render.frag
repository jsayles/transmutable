{% load imagetags %}
{% load wikitags %}
<script>
$(document).ready(function() {
	{% if is_mobile %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.mobile_views.wiki_edit page.namespace.name page.name %}";
		});
	{% else %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_edit page.namespace.owner.username page.namespace.name page.name %}";
		});
		$('button[name="print-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_print page.namespace.owner.username page.namespace.name page.name %}";
		});
		$('button[name="history-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_history page.namespace.owner.username page.namespace.name page.name %}";
		});
	{% endif %}
});
</script>

	{% if not hide_title %}
		<ul class="breadcrumb">
			{% if request.user.is_authenticated %}
			<li>
				<a href="{% url peach.views.index %}">Notes</a> <span class="divider">/</span>
			</li>
			{% endif %}			
			<li><a href="{{page.namespace.get_absolute_url}}">{{ page.namespace.display_name }}</a> <span class="divider">/</span></li>
			<li class="active">{{ page.name }}</li>
		</ul>
	{% endif %}

	{% if request.user.is_authenticated and page.namespace.owner.username == request.user.username %}
		<div class="wiki-control-links">
		<a href="{% url peach.views.wiki_edit page.namespace.owner.username page.namespace.name page.name %}">
			<i class="icon-edit" alt="edit"></i> edit
		</a>
		{% if not is_mobile %}
			<a href="{% url peach.views.wiki_print page.namespace.owner.username page.namespace.name page.name %}" target="_new">
				<i class="icon-print" alt="print"></i> print
			</a>
			<a href="{% url peach.views.wiki_history page.namespace.owner.username page.namespace.name page.name %}">
				<i class="icon-time" alt="history"></i> history
			</a>
		{% endif %}
		</div> 
	{% endif %}

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
