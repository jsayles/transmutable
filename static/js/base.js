// Javascript for the entire project

var transmutable = transmutable || {};

transmutable.views = transmutable.views || {};

transmutable.views.FormattingHelpView = Backbone.View.extend({
	className: 'formatting-help alert alert-info',
	initialize: function(){
		_.bindAll(this);
		var closeButton = $.el.button({'type':'button', 'class':'close', 'data-dismiss':'alert'});
		closeButton.innerHTML = '&times;';
		this.$el.append(closeButton);
		this.$el.append($.el.h4('Formatting help'));

		this.$el.append($('<h3>Use # for headings</h3> # Biggest<br/> ## Second Biggest<br/> ### Third Biggest<br/> <h3>Use - for lists</h3> - Apples<br/> - Oranges<br/> - Aesthetics<br/> <h3>Create links</h3> [Example](http://exa.com) <p style="margin-top: 2em;">See the <a target="_new" href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> page for more options.</p>'));
	},
	render: function(){
		return this;
	}
})

transmutable.views.GenericCollectionView = Backbone.View.extend({
	tagName: 'ul',
	className: 'collection-view',
	initialize: function(){
		_.bindAll(this);
		this.itemViews = [];
		this.collection.on('reset', this.handleSync);
		this.collection.on('sync', this.handleSync);
		this.collection.on('remove', this.handleRemove);
	},
	getItemView: function(model){
		for(var i=0; i < this.itemViews.length; i++){
			if(this.itemViews[i].model == model) return this.itemViews[i];
		}
		return null;
	},
	addOne: function(model){
		var itemView = this.itemViews[this.itemViews.length] = new this.options.itemClass({
			'model':model,
			'collection':this.collection
		});
		this.$el.append(itemView.el);
	},
	handleRemove: function(model){
		var itemView = this.getItemView(model);
		if(!itemView) return;
		this.itemViews = _.without(this.itemViews, itemView);
		itemView.$el.remove();
	},
	handleSync: function(){
		for(var i=0; i < this.itemViews.length; i++){
			this.itemViews[i].remove();
		}
		this.itemViews = [];
		for(var i=0; i < this.collection.length; i++){
			this.addOne(this.collection.at(i));
		}
		this.collection.on('add', this.addOne);
	}
})

transmutable.getCookie = function(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

transmutable.MultipartUploader = function(data, progressCallback, destinationURL, method){
	/*
	This uploads data (which should be a map) using the multipart form encoding.
	Any values in the data which are files are loaded using FileReaders.
	*/
	this.method = method || 'POST';
	this.progressCallback = progressCallback;
	this.boundary = '------multipartformboundary' + (new Date).getTime();
	this.destinationURL = destinationURL || '.';
	this.percentage = 0;
	this.filesRead = 0;
	this.files = {};
	this.body = '';
	this.xhr = new XMLHttpRequest();

	this.progressFunction = function(event) {
		if (event.lengthComputable) {
			this.percentage = Math.round((event.loaded * 100) / event.total);
			if(this.percentage == 100) return; // The loadFunction calls it with 100%
			if(this.progressCallback) this.progressCallback(this, this.percentage);
		}
	};
	this.xhr.upload.addEventListener("progress", _.bind(this.progressFunction, this), false);

	this.handleReadyStateChange = function(event){
		if(this.xhr.readyState == 4 && this.xhr.status == 200) this.loadFunction();
		if(this.xhr.readyState == 4 && this.xhr.status != 200) this.errorFunction();
	}
	this.xhr.onreadystatechange = _.bind(this.handleReadyStateChange, this);

	this.errorFunction = function(e){
		this.percentage = -1;
		if(this.progressCallback) this.progressCallback(this, this.percentage);
	};
	
	this.loadFunction = function(e){
		this.percentage = 100;
		if(this.progressCallback) this.progressCallback(this, this.percentage);
	};
	
	this.handleFileLoaded = function(event){
		var reader = event.target;
		this.body = this.body + transmutable.serializeForPost(reader._file.name, reader.result, this.boundary, reader._parameterName, 'application/octet-stream');
		this.filesRead += 1;
		if(this.filesRead == Object.keys(this.files).length) this.startUpload();
	};

	// Called to start the upload
	// If there are files in the data, this is called once all of the FileReaders are finished loading
	this.startUpload = function(){
		this.xhr.open(this.method, this.destinationURL, true);
		this.xhr.setRequestHeader('content-type', 'multipart/form-data; boundary=' + this.boundary);
		this.xhr.setRequestHeader("X-CSRFToken", transmutable.getCookie('csrftoken')); // This is for Django's XSS middleware
		this.xhr.sendAsBinary(this.body, 'multipart/form-data');
	};

	for(var key in data){
		if(data[key] == null){
			// pass
		} else if(typeof data[key] == 'object'){
			this.files[key] = data[key];
		} else {
			this.body = this.body + transmutable.serializeForPost(null, data[key], this.boundary, key, 'text/plain');
		}
	}
	if(Object.keys(this.files).length == 0){
		this.startUpload();
	} else {
		for(var key in this.files){
			var reader = new FileReader();
			reader._file = this.files[key];
			reader._parameterName = key;
			reader.onload = _.bind(this.handleFileLoaded, this);
			reader.readAsArrayBuffer(this.files[key]);
		}
	}
}

transmutable.serializeForPost = function(filename, data, boundary, parameterName, contentType) {
	/*
	Create a multipart POST body which encodes the data
	*/
	var dashdash = '--';
	var crlf = '\r\n';
	var builder = '';

	builder += dashdash;
	builder += boundary;
	builder += crlf;
	builder += 'Content-Disposition: form-data; name="' + parameterName + '"';
	if(filename) builder += '; filename="' + filename + '"';
	builder += crlf;

	builder += 'Content-Type: ' + contentType;
	builder += crlf;
	builder += crlf; 

	if (typeof data==="object") {
		builder += transmutable.packBytes(new Uint8Array(data));
	} else {
		builder += data
	}
	builder += crlf;

	builder += dashdash;
	builder += boundary;
	builder += dashdash;
	builder += crlf;
	return builder;
}

transmutable.packBytes = function(bytes) {
	var str = "";
	for(var i = 0; i < bytes.length; i += 1) {
		str += String.fromCharCode(bytes[i]);
	}
	return str;
}

if (XMLHttpRequest.prototype) {
	XMLHttpRequest.prototype.sendAsBinary = function(text, mimeType){
		/*
		A utility function to convert text to a blob
		*/
		var data = new ArrayBuffer(text.length);
		var ui8a = new Uint8Array(data, 0);
		for (var i = 0; i < text.length; i++) ui8a[i] = (text.charCodeAt(i) & 0xff);
		this.send(new Blob([data], {"type": mimeType}));
	}
}

$.urlVars = function(){
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	for(var i = 0; i < hashes.length; i++) {
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = unescape(hash[1]);
	}
	return vars;
};

$.urlVar = function(name){
	return $.urlVars()[name];
};

$.isMobile = function(){
	return navigator.userAgent.toLowerCase().match(/(iPhone|iPod|iPad|blackberry|android|htc|kindle|lg|midp|mmp|mobile|nokia|opera mini|palm|pocket|psp|sgh|smartphone|symbian|treo mini|Playstation Portable|SonyEricsson|Samsung|MobileExplorer|PalmSource|Benq|Windows Phone)/i);
};

window.console = console||{'log':function(){}}; // Because IE does not create the console API until you actually show the console UI!

(function(doc){
	var write = doc.write;
	doc.write = function(q){ 
		if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);  
	};
})(document);

window.schema = new phlogiston.TastyPieSchema(null, {'url':'/api/v0.1/'});
window.urlLoader = new phlogiston.UrlLoader(null, {'url':'/phlogiston/url/'})

$(document).ready(function(){
	window.urlLoader.on('populated', function(){
		window.schema.fetch({
			'error': function(){
				console.log("Could not fetch the tasty pie schema", arguments);
			}
		});
	});
	window.urlLoader.fetch({
		'error': function(){ console.log("Could not fetch the url loader data", arguments); }
	});

	//transmutable.initSearch();
});
