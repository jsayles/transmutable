<form class="search-form" action="{% url search_views.search %}" method="post">
	{% for field in search_form %}{{ field }}{% endfor %}
</form>
