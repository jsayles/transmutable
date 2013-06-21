<div class="user-item update-view">
	{% if show_user %}
		{% include "banana/user_photo_small.frag" %}
		<a href="{{ user.get_absolute_url }}">{{ user.get_full_name }}</a>
	{% endif %}
	<div class="rendered">
		{% if user.get_profile.bio %}
			{{ user.get_profile.bio|striptags|truncatewords:"30" }}
		{% endif %}
	</div>
</div>
