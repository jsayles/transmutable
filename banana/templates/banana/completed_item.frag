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
		<div class="completed-item-meta-timestamp">{{ completed_item.created|timesince }} ago</div>
		{% if not hide_completed_item_info_button %}
			<a class="completed-item-meta-button completed-item-info-button" href="{{ completed_item.get_absolute_url }}">info</a>
		{% endif %}
		{%if rocked_it %}
			<span class="completed-item-meta-button completed-item-rock-button">
				Rocked!
				{% if completed_item.rock_count %}({{ completed_item.rock_count}}){% endif %}
			</span>
		{% else %}
			{% if request.user.is_authenticated %}
				{% if completed_item.user == request.user %}
					{% if completed_item.rock_count %}
						<span class="completed-item-meta-button completed-item-rock-button">
							Rocked! ({{ completed_item.rock_count}})
						</span>
					{% endif %}
				{% else %}
					<a id="completed-item-rock-button-{{completed_id.id}}" href="." class="completed-item-meta-button completed-item-rock-button" onclick="rockCompletedItem({{ completed_item.id }}, {{ completed_item.rock_count}}, this); return false;">
						Rock!
						{% if completed_item.rock_count %}({{ completed_item.rock_count}}){% endif %}
					</a>
				{% endif %}
			{% endif %}
		{% endif %}

	</div>
</li>