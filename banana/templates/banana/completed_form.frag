<form id="completed-form" action="." method="post">
	<h2 class="completed-form-heading">So, what'd you do?</h2>
	{{ completed_form.markup }}
	<br clear="all" />
	<button name="completed-form-button" type="button" class="positive">to-done!</button>
	{% if request.user.has_unused_tada %}
		<div id="promoted-ui">
			{{ completed_form.promoted }} ta-da!
		</div>
		<div id="promoted-extended-ui">
			<span>Enter a link to promote your achievement!</span>
			{{ completed_form.link }}
		</div>
	{% endif %}
</form>
