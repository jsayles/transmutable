{% load imagetags %}
<div class="gratitude-item update-view">
	{% if show_user %}
		{% if gratitude.user.get_profile.photo %}
			<a href="{{ gratitude.user.get_absolute_url }}"><img class="person-photo" src="{{ gratitude.user.get_profile.photo.image.url|fit_image:"50x50" }}" title="{{ gratitude.user.get_full_name}}" alt="{{ gratitude.user.get_full_name}}" /></a>
		{% else %}
			<a href="{{ gratitude.user.get_absolute_url }}"><img class="person-photo" src="{{STATIC_URL}}person/BlankIcon150x150.jpg" width="50" height="50" /></a>
		{% endif %}
		<a href="{{ gratitude.user.get_absolute_url }}">{{ gratitude.user.get_full_name }}</a>
	{% endif %}
	<div class="rendered">
		{{ gratitude.rendered|safe }}
	</div>
	{% if not hide_meta %}
		<div class='update-meta'>
			<div class="update-timestamp">
				<a href="{{ gratitude.get_absolute_url }}">
					{{ gratitude.created|timesince }} ago
				</a>
			</div>
		</div>
	{% endif %}
</div>
