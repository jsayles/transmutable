{% load imagetags %}
<li class="completed-item-li rendered-wrapper">
	{% if show_completed_item_user %}
		{% if completed_item.user.get_profile.photo %}
			<a href="{{ completed_item.user.get_absolute_url }}"><img class="person-photo" src="{{ completed_item.user.get_profile.photo.image.url|fit_image:"50x50" }}" title="{{ completed_item.user.get_full_name}}" alt="{{ completed_item.user.get_full_name}}" /></a>
		{% else %}
			<a href="{{ completed_item.user.get_absolute_url }}"><img class="person-photo" src="{{ MEDIA_URL }}person/BlankIcon150x150.jpg" width="50" height="50" /></a>
		{% endif %}
		<a href="{{ completed_item.user.get_absolute_url }}">{{ completed_item.user.get_full_name }}</a>
	{% endif %}
	{{ completed_item.rendered|safe }}
	<div class="completed-item-meta">
		<span class="completed-item-meta-timestamp">{{ completed_item.created|timesince }} ago</span>
		<a class="completed-item-meta-button completed-item-info-button" href="{{ completed_item.get_absolute_url }}">INFO</a>
		{% if request.user.is_authenticated and not completed_item.user == request.user %}
			{% comment %}<a href="." class="completed-item-meta-button completed-item-rock-button" onclick="rockCompletedItem({{ completed_item.id }}); return false;">Rock!</a>{% endcomment %}
		{% endif %}
	</div>
</li>