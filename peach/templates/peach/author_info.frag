{% load imagetags %}
<div class="author-info">
	{% if author.get_profile.photo %}
	<a href="{{ author.get_absolute_url }}"><img class="person-photo" src="{{ author.get_profile.photo.image.url|thumbnail:"130w" }}" width="130" title="{{ author.get_full_name}}" alt="{{ author.get_full_name}}" /></a>
	{% else %}
	<a href="{{ author.get_absolute_url }}"><img class="person-photo" src="{{ MEDIA_URL }}person/BlankIcon150x150.jpg" width="130" height="130" /></a>
	{% endif %}
	<h3><a href="{{ author.get_absolute_url }}">{{ author.get_full_name }}</a></h3>
</div>