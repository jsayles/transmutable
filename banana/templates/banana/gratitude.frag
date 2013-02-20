<div class="gratitude-item update-view">
	<div class="rendered">
		{{ gratitude.rendered|safe }}
	</div>
	<div class='update-meta'>
		<div class="update-timestamp">
			<a href="{{ gratitude.get_absolute_url }}">
				{{ gratitude.created|timesince }} ago
			</a>
		</div>
	</div>
</div>
