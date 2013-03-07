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

transmutable.createUrlFuction = function(patternInfo, prefix){
    return function(){
        if(arguments.length != patternInfo.groups.length){
            throw "Expected arguments: (" + patternInfo.groups.join(',') + ")";
        }
        for(var i=0; i < arguments.length; i++){
            if(typeof arguments[i] == 'undefined'){
                console.log('Undefined arguments', arguments);
                throw 'Passed an undefined argument: ' + arguments;
            }
        }
        var tokens = transmutable.splitRegex(patternInfo.regex);
        var url = '';
        var groupIndex = 0;
        for(var i=0; i < tokens.length; i++){
            if(tokens[i] == null){ // it's a group, add from args 
                url += arguments[groupIndex];
                groupIndex++;
            } else { // it's a token, add it to the URL
                url += tokens[i];
            }
        }
        if(!prefix) prefix = ''
        return prefix + url;
    }
};

transmutable.splitRegex = function(regex){
    /*
    Takes a regex string like '^views/(?P<view>[^/]+)/$' and returns an array of elements like ["views/", null, "/"]
    */
    if(regex.charAt(0) == '^') regex = regex.slice(1);
    if(regex.charAt(regex.length - 1) == '$') regex = regex.slice(0, regex.length - 1);
    results = []
    line = ''
    for(var i =0; i < regex.length; i++){
        var c = regex.charAt(i);
        if(c == '('){
            results[results.length] = line;
            results[results.length] = null;
            line = '';
        } else if(c == ')'){
            line = '';
        } else {
            line = line + c;
        }
    }
    if(line.length > 0) results[results.length] = line
    return results
}

transmutable.cleanPathElement = function(element){
    return element.replace('-', '_');
}

transmutable.UrlLoader = Backbone.Model.extend({
    /*
    This object reads the URL resource from the server and populates transmutable.urls with functions which return URLs.
    */
    url:'{% url backbone.views.urls %}',
    initialize: function(options){
        this.on('change', this.populate);
    },
    populate: function(){
        var patterns = this.get('patterns');
        for(var i=0; i < patterns.length; i++){
            transmutable.urls[transmutable.cleanPathElement(patterns[i].name)] = transmutable.createUrlFuction(patterns[i], '/');
        }
        var resolvers = this.get('resolvers');
        for(var i=0; i < resolvers.length; i++){
            var resolver_patterns = {};
            var resolverPrefix = transmutable.createUrlFuction(resolvers[i], '/')()
            for(var j=0; j < resolvers[i].patterns.length; j++){
                var pattern = resolvers[i].patterns[j];
                resolver_patterns[transmutable.cleanPathElement(pattern.name)] = transmutable.createUrlFuction(pattern, resolverPrefix)
            }
            transmutable.urls[transmutable.cleanPathElement(resolvers[i].name)] = resolver_patterns;
        }
    }
});
transmutable.URL_LOADER = new transmutable.UrlLoader();
$(document).ready(function(){
    transmutable.URL_LOADER.fetch();
});

transmutable.urls.wikiPage = function(username, namespace, name){
	var url = transmutable.replaceID("{% url peach.views.wiki 333 666 999 %}", 333, username);
    url = transmutable.replaceID(url, 666, namespace);
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
