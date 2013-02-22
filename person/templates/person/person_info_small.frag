{% load imagetags %}
<div class="person-info-small">
	{% if profile_link %}<a href="{{ profile_link }}">{% endif %}
	{% if profile.photo %}
	<img class="person-photo" src="{{ profile.photo.image.url|thumbnail:"75w" }}" width="75" title="{{profile.user.get_full_name}}" alt="{{ profile.get_full_name}}" />
	{% else %}
	<img class="person-photo" src="{{STATIC_URL}}person/BlankIcon150x150.jpg" width="75" height="75" />		
	{% endif %}
	{% if profile_link %}</a>{% endif %}
	
	<h2 class="vcard">
		<span class="fn">
			{% if profile_link %}<a href="{{ profile_link }}">{% endif %}
			{{ profile.user.get_full_name }}
			{% if profile_link %}</a>{% endif %}
		</span>
	</h2>
	<table>
		{% if profile.location %}
			<tr><th>Location:</th><td>{{ profile.location }}</td></tr>
		{% endif %}
		{% if profile.url %}
			<tr><th>URL:</th><td>{{ profile.url|urlize }}<td></tr>
		{% endif %}
		{% if profile.bio %}
			<tr><td colspan="2">{{ profile.bio|truncatewords:"8" }}</td></tr>
		{% endif %}
	</table>
	<br clear="all" />
</div>
