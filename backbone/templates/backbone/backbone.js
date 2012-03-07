/* The Backbone.js resource wrappers */

var transmutable = transmutable || {};
{% for api_form in api_forms %}

transmutable.{{api_form.form_name}} = Backbone.Model.extend({
{% if api_form.url %}
	url: "{{api_form.url}}",
{% else %}
	{% if api_form.url_id_field %}urlIdField: "{{ api_form.url_id_field }}",{% endif %}
	url: function(){
		if(this.isNew()) return this.collectionUrl();
		var urlToken = 'id';
		if(typeof this.urlIdField != 'undefined') urlToken = this.urlIdField;
		return transmutable.replaceID("{{api_form.resource_url}}", "1234", this.get(urlToken));
	},
	
	collectionUrl: function(){
		return transmutable.replaceID("{{api_form.collection_url}}", "1234", this.urlId);
	},
{% endif %}
});

{% if api_form.collection_url or api_form.base_url %}
transmutable.{{api_form.form_name}}Collection = Backbone.Collection.extend({
{% if api_form.collection_url %}
	url: function(){
		return transmutable.replaceID("{{api_form.collection_url}}", "1234", this.urlId);
	}
{% endif %}
});
{% endif %}

{% endfor %}


transmutable.urls = {};

transmutable.urls.wikiPage = function(namespace, name){
	var url = transmutable.replaceID("{% url peach.views.wiki 666 999 %}", 666, namespace);
	return transmutable.replaceID(url, 999, name);
}

transmutable.replaceID = function(data, id, newValue){ return data.replace(new RegExp(id, "g"), newValue); }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

function safeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Make all jQuery ajax send the XCSRF token
$(document).on('ajaxSend', function(event, xhr, settings) {
	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});
