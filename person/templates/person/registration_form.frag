<form onsubmit="$('#registration-form-submit').attr('disabled', 'disabled');" id="registration-form" action="{% url person.views.register %}" method="post">
	<table>
		{{ registration_form }}
		<tr><td colspan="2" style="text-align: right;"><input id="registration-form-submit" type="submit" value="sign up" /></td>
	</table>
	{% csrf_token %}
</form>
