<li class="completed-item-li rendered-wrapper">
	{{ completed_item.rendered|safe }}
	<div class="completed-item-meta"><a href="{{ completed_item.get_absolute_url }}">{{ completed_item.modified|timesince }} ago</a></div>
</li>