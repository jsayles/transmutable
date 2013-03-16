// Javascript for the entire project

var transmutable = transmutable || {};

transmutable.views = transmutable.views || {};

transmutable.views.FormattingHelpView = Backbone.View.extend({
	className: 'formatting-help alert alert-info',
	initialize: function(){
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

window.log = function(){
	log.history = log.history || []; 
	log.history.push(arguments);
	if(this.console){
		console.log( Array.prototype.slice.call(arguments) );
	}
};

(function(doc){
	var write = doc.write;
	doc.write = function(q){ 
		if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);  
	};
})(document);

//$(document).ready(function(){
//	transmutable.initSearch();
//});

