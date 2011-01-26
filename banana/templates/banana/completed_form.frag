<form id="completed-form" action="." method="post">
	<h2 class="completed-form-heading">So, what'd you do?</h2>
	{% for field in completed_form %}{{ field }}{% endfor %}
	<br clear="all" />
	<button name="completed-form-button" type="button" class="positive">to-done!</button>
</form>
