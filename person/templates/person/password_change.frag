{% load imagetags %}
<form id="password-change-form" action="{% url person.views.password_edit %}" method="post">
<table>
{{ password_change_form }}
<tr>
	<td colspan="2">
		<input type="hidden" name="password_change_form" value="True" />
		<input type="submit" value="change your password" />
	</td>
</tr>
</table>
{% csrf_token %}
</form>
