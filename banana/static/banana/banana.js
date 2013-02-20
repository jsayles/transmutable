var banana = banana || {};
banana.views = banana.views || {};
banana.models = banana.models || {};

banana.models.CompletedItem = Backbone.Model.extend({
	url:function(){
		if(this.isNew()) return '/api/completed-item/';
		return '/api/completed-item/' + this.id;
	}
});
banana.models.CompletedItemCollection = Backbone.Collection.extend({
	url: '/api/completed-item/'
});

banana.models.Gratitude = Backbone.Model.extend({
	url:function(){
		if(this.isNew()) return '/api/gratitude/';
		return '/api/gratitude/' + this.id;
	}
});
banana.models.GratitudeCollection = Backbone.Collection.extend({
	url: '/api/gratitude/'
});

banana.views.CompletedItemEditView = Backbone.View.extend({
	tagName: 'form',
	className: 'completed-item-edit-view update-edit-view',
	initialize: function(options){
		_.bindAll(this);
		if(!this.model) this.makeNewModel();

		this.$el.attr('action', '.');
		this.$el.attr('method', 'post');

		this.textArea = $.el.textarea({'name':'markup', 'placeholder':'Some awesome thing I did...'}, this.model.get('markup'));
		this.$el.append(this.textArea);

		this.submitButton = $.el.button({'name':'submit-form-button', 'type':'submit'}, 'to-done!');
		$(this.$el).submit(this.handleSubmit);
		this.$el.append(this.submitButton);

		this.promotedCheckbox = $.el.input({'type':'checkbox', 'name':'promoted'});
		if(this.model.get('promoted')){
			$(this.promotedCheckbox).attr('checked', 'checked');
		}
		$(this.promotedCheckbox).click(this.toggleTada);
		if(this.options.hasTada){
			this.$el.append(this.promotedCheckbox);
			this.$el.append($.el.label({'for':'promoted'}, 'ta-da!'));
		}
		this.linkInput = $.el.input({'type':'text', 'name':'link', 'placeholder':'optional link to promote'});
		$(this.linkInput).val(this.model.get('link'));
	},
	makeNewModel: function(){
		this.options.model = this.model = new banana.models.CompletedItem();
	},
	toggleTada: function(){
		if($(this.promotedCheckbox).attr('checked') == 'checked'){
			this.$el.append(this.linkInput);
		} else {
			$(this.linkInput).remove();
		}
	},
	saveSucceeded: function(){
		if(this.options.successCallback){
			this.options.successCallback(this.model);
		}
		this.makeNewModel();
	}, 
	saveFailed: function(){
		console.log('error', arguments);
	},
	handleSubmit: function(){
		var changeData = {
			'markup':$(this.textArea).val()
		};
		if($(this.promotedCheckbox).attr('checked') == 'checked'){
			changeData['promoted'] = true;
			var link = $(this.linkInput).val().trim();
			if(link.length > 0){
				changeData['link'] = link;
			}
			$(this.promotedCheckbox).remove();
			this.$el.find('label[for=promoted]').remove();
			$(this.linkInput).remove();
		}
		this.model.save(changeData, {
			'success':this.saveSucceeded,
			'error':this.saveFailed
		});
		$(this.textArea).val('');
		return false;
	}
});

banana.views.CompletedItemView = Backbone.View.extend({
	className: 'completed-item-view update-view',
	initialize: function(options){
		_.bindAll(this);
		this.rendered = $.el.div({'class':'rendered'});
		$(this.rendered).html(this.model.get('rendered'));
		this.$el.append(this.rendered);

		this.metaData = $.el.div({'class':'update-meta'});
		this.$el.append(this.metaData);

		if(this.model.get('link')){
			this.metaData.append($.el.div({'class':'promoted-link update-meta-button'}, $.el.a({'href':this.model.get('link'), 'rel':'nofollow'}, $.el.i({'class':'icon-external-link'}))));
		}
		this.metaData.append($.el.div({'class':'update-timestamp'}, $.el.a({'href':transmutable.urls.banana.completed_item(this.model.id)}, $.timeago(this.model.get('created')))));
		if(this.model.get('promoted')){
			this.$el.addClass('promoted');
		}

		if(this.model.get('rock_count') > 0){
			this.$el.append($.el.div({'class':'completed-item-rock'}, 'Rocked! (' + this.model.get('rock_count') + ')'))
		}
	}
});

banana.views.CompletedItemsView = Backbone.View.extend({
	className: 'completed-items-view updates-view',
	initialize: function(options){
		_.bindAll(this);
		this.childrenViews = [];
		this.maxLength = this.options.maxLength || 10;
		this.listenTo(this.collection, 'reset', this.handleReset);
	},
	handleReset: function(){
		for(var i=0; i < this.childrenViews.length; i++){
			this.childrenViews[i].remove();
		}
		this.childrenViews = [];
		for(var i=0; i < this.collection.length && i < this.maxLength; i++){
			this.addOne(this.collection.at(i));
		}
	},
	addOne: function(model){
		var view = new banana.views.CompletedItemView({
			'model':model
		})
		this.childrenViews[this.childrenViews.length] = view;
		this.$el.append(view.el);
		return view;
	}
})

banana.views.GratitudeEditView = Backbone.View.extend({
	tagName: 'form',
	className: 'gratitude-edit-view update-edit-view',
	initialize: function(options){
		_.bindAll(this);
		if(!this.model) this.makeNewModel();

		this.$el.attr('action', '.');
		this.$el.attr('method', 'post');

		this.textArea = $.el.textarea({'name':'markup', 'placeholder':'I\'m grateful for...'}, this.model.get('markup'));
		this.$el.append(this.textArea);

		this.submitButton = $.el.button({'name':'submit-form-button', 'type':'submit'}, 'thanks!');
		$(this.$el).submit(this.handleSubmit);
		this.$el.append(this.submitButton);
	},
	makeNewModel: function(){
		this.options.model = this.model = new banana.models.Gratitude();
	},
	saveSucceeded: function(){
		if(this.options.successCallback){
			this.options.successCallback(this.model);
		}
		this.makeNewModel();
	}, 
	saveFailed: function(){
		console.log('error', arguments);
	},
	handleSubmit: function(){
		this.model.save({ 'markup':$(this.textArea).val() }, {
			'success':this.saveSucceeded,
			'error':this.saveFailed
		});
		$(this.textArea).val('');
		return false;
	}
});

banana.views.GratitudeView = Backbone.View.extend({
	className: 'gratitude-view update-view',
	initialize: function(options){
		_.bindAll(this);

		this.rendered = $.el.div({'class':'rendered'});
		$(this.rendered).html(this.model.get('rendered'));
		this.$el.append(this.rendered);

		this.metaData = $.el.div({'class':'update-meta'});
		this.$el.append(this.metaData);
		this.metaData.append($.el.div({'class':'update-timestamp'}, $.el.a({'href':transmutable.urls.banana.gratitude(this.model.id)}, $.timeago(this.model.get('created')))));
	}
});

banana.views.GratitudesView = Backbone.View.extend({
	className: 'gratitudes-view updates-view',
	initialize: function(options){
		_.bindAll(this);
		this.childrenViews = [];
		this.maxLength = this.options.maxLength || 10;
		this.listenTo(this.collection, 'reset', this.handleReset);
	},
	handleReset: function(){
		for(var i=0; i < this.childrenViews.length; i++){
			this.childrenViews[i].remove();
		}
		this.childrenViews = [];
		for(var i=0; i < this.collection.length && i < this.maxLength; i++){
			this.addOne(this.collection.at(i));
		}
	},
	addOne: function(model){
		var view = new banana.views.GratitudeView({
			'model':model
		})
		this.childrenViews[this.childrenViews.length] = view;
		this.$el.append(view.el);
		return view;
	}
})