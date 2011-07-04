<form id="profile-form" action="." method="post">
<table>
	{{ profile_form }}
	<tr><td colspan="2" style="text-align: right;"><button type="submit">save your profile</button></td></tr>
</table>
{% csrf_token %}
</form>