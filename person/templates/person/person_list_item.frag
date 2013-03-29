{% load imagetags %}
<li class="person-list-item">
	{% if profile_link %}<a href="{{ profile_link }}">{% endif %}
	{% if profile.photo %}
		<img class="person-photo" src="{{ profile.photo.image.url|thumbnail:"75w" }}" width="75" title="{{profile.user.get_full_name}}" alt="{{ profile.get_full_name}}" />
	{% else %}
		<img class="person-photo" src="{{STATIC_URL}}person/BlankIcon150x150.jpg" width="75" height="75" />		
	{% endif %}
	{% if profile_link %}</a>{% endif %}
	
	<h4 class="vcard">
		<span class="fn">
			{% if profile_link %}<a href="{{ profile_link }}">{% endif %}
			{{ profile.user.get_full_name }}
			{% if profile_link %}</a>{% endif %}
		</span>
	</h4>
</li>
