<form id="completed-form" action="." method="post">
	{{ completed_form.markup }}
	<br clear="all" />
	<button name="completed-form-button" type="submit" class="positive">to-done!</button>
	{% if request.user.has_unused_tada %}
		<div id="promoted-ui">
			{{ completed_form.promoted }} ta-da!
		</div>
		<div id="promoted-extended-ui">
			{{ completed_form.link }}
		</div>
	{% endif %}
</form>
