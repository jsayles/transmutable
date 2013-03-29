var transmutable = transmutable || {};

transmutable.WikiPageEditView = Backbone.View.extend({
	
	className: 'wikiPageEditor',

	events: {
		'click button.save-button': 'save',
		'click button.save-and-close-button': 'saveAndClose',
	},

	initialize: function(){
		_.bindAll(this, 'render', 'save', 'saveAndClose');
		this.model = new transmutable.WikiPage({id:this.options.wikiPageId});
		this.model.bind('change', this.render, this);
		this.model.fetch();
	},

	save: function(){
		this.model.attributes.content = this.$('#id_content').val();
		this.model.save(null, {
			error: function(model, response) {
				console.log("Error", model, response);
			},
			success: function(model, response) {
				//this.$('.save-button').fadeOut(100).fadeIn(1000);
			}
		});
	},
	
	saveAndClose: function(){
		this.model.attributes.content = this.$('#id_content').val();
		var self = this;
		this.model.save(null, {
			error: function(model, response) {
				console.log("Error", model, response);
			},
			success: function(model, response) {
				document.location.href = transmutable.urls.wikiPage(self.options.username, self.options.namespace, self.options.name);
			}
		});
	},

	render: function(){
		var el = $(this.el);
		el.empty();
		var form = $('<form id="page-form" action="." method="post">');
		var textArea = $('<textarea id="id_content" name="content"></textarea>');
		textArea.text(this.model.attributes.content);
		form.append(textArea);
		el.append(form);
		el.append('<button type="buttom" class="save-button">Save</button>');
		el.append('<button type="buttom" class="save-and-close-button">Save and Close</button>');
		$(textArea).focus()
	}
});