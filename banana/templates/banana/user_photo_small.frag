{% load imagetags %}
{% if user.get_profile.photo %}
	<a href="{{ user.get_absolute_url }}"><img class="person-photo" src="{{ user.get_profile.photo.image.url|fit_image:"50x50" }}" title="{{ user.get_full_name}}" alt="{{ user.get_full_name}}" /></a>
{% else %}
	<a href="{{ user.get_absolute_url }}"><img class="person-photo" src="{{STATIC_URL}}person/BlankIcon150x150.jpg" width="50" height="50" /></a>
{% endif %}
