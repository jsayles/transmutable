<form class="search-form" action="{% url backbone.views.search %}" method="post">
	{% for field in search_form %}{{ field }}{% endfor %}
</form>
