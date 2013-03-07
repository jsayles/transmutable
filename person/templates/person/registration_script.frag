{% if terms_of_service_url %}
	var tosURL = '{{ terms_of_service_url }}';
{% else %}
	var tosURL = null;
{% endif %}

$(document).ready(function() {
	$('label[for=id_tos]').hide();
	if(tosURL){
		$('#id_tos').after($.el.span('I accept the ', $.el.a({'href':tosURL, 'target':'_new'}, 'terms of service'), '.'));
	} else {
		$('#id_tos').after($.el.span('I accept the terms of service.'));
	}
	$('#id_username').focus();
	$('#registration-form').submit(function(){
		$('#registration-form-submit').attr('disabled', 'disabled');
		return true;
	})
});
