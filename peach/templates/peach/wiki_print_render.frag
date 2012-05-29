{% load imagetags %}
{% load wikitags %}
{% if not hide_title %}<h1><a style="color: #000; font-size: 1.2em;" href="{{page.get_absolute_url }}">{{ page.name }}</a> </h1>{% endif %}

{% if page.rendered %}
	<div class="rendered-wrapper printed-page">{{ page.rendered|include_constants|safe }}</div>
{% endif %}
