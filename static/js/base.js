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
