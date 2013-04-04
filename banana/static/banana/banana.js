var banana = banana || {};
banana.views = banana.views || {};
banana.models = banana.models || {};

window.tastyPieSchema.once('populated', function(){
	phlogiston.banana.CompletedItemCollection.prototype.comparator = function(completedItem){
		return -1 * phlogiston.parseJsonDate(completedItem.get('created')).getTime();		
	}
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

banana.models.WorkDoc = Backbone.Model.extend({
	url:function(){ return '/api/work-doc/'; }
});

banana.views.NewUserTourView = Backbone.View.extend({
	className: 'new-user-tour-view',
	initialize: function(options){
		_.bindAll(this);
		this.completed = false;

		this.titleRow = $.el.div(
			{'class':'row-fluid new-user-tour-title-row'}, 
			$.el.h2({'class':'span12'}, 'Let\'s get started with ' + this.options.siteName + '!')
		);
		this.$el.append(this.titleRow);

		this.congratulationsRow = $.el.div(
			{'class':'row-fluid new-user-tour-congratulations-row'}, 
			$.el.h2({'class':'span12'}, 'That\'s the core of Transmutable Work.  Keep going!')
		);
		this.$el.append(this.congratulationsRow);

		this.toDoCopy = $.el.div({'class':'new-user-copy'}, 'Offload your upcoming to-do\'s and relevant info.');
		this.toDoneCopy = $.el.div({'class':'new-user-copy'}, 'Now celebrate some task you finished by writing it below.');
		this.gratitudesCopy = $.el.div({'class':'new-user-copy'}, 'Now give thanks for one of your many helpful people or tools.');

		$('#work-doc-column .section-title').html('1. ' + $('#work-doc-column .section-title').html());
		$('#completed-column .section-title').html('2. ' + $('#completed-column .section-title').html());
		$('#gratitudes-column .section-title').html('3. ' + $('#gratitudes-column .section-title').html());
		$('#completed-column').hide();
		$('#gratitudes-column').hide();
		this.$el.find('.new-user-tour-title-row').show();
		this.$el.find('.new-user-tour-congratulations-row').hide();

		this.showStepOne();
	},
	showStepOne: function(){
		if(this.completed) return;
		$('#edit-work-doc-link').hide();
		$('.new-user-copy').remove();
		$('#work-doc-column .section-title').append(this.toDoCopy);
		$('#work-doc-column').show().addClass('offset4');
	},
	showStepTwo: function(){
		if(this.completed) return;
		$('#work-doc-column').show().removeClass('offset4');
		$('#completed-column .section-title').append(this.toDoneCopy);
		$('#completed-column').show();
	},
	showStepThree: function(){
		if(this.completed) return;
		$('#gratitudes-column').show();
		$('#gratitudes-column .section-title').append(this.gratitudesCopy);
	},
	showStepFour: function(){
		if(this.completed) return;
		this.completed = true;
		this.$el.find('.new-user-tour-title-row').hide();
		this.$el.find('.new-user-tour-congratulations-row').show();

		setTimeout(_.bind(function(){
			this.$el.find('.new-user-tour-congratulations-row').hide(400);
			$('.new-user-copy').hide(400);
			
		}, this), 5000);
	}
});

banana.views.WorkDocEditView = Backbone.View.extend({
	className: 'work-doc-edit-view',
	initialize: function(options){
		_.bindAll(this);
		this.form = $.el.form({'action':'.', 'method':'post'},
			$.el.textarea({'name':'markup', 'placeholder':'- Check out sciencesaints.com'}),
			$.el.a({'id':'formatting-help-link', 'href':'.'}, 'formatting help')
		);
		this.saveButton = $.el.button({'accesskey':'s', 'name':'work-doc-save-button', 'type':'button', 'class':'btn'}, 'save'),
		this.form.append(this.saveButton);
		$(this.saveButton).click(this.save);
		this.cancelButton = $.el.button({'name':'work-doc-cancel-button', 'type':'button', 'class':'btn'}, 'cancel')
		this.form.append(this.cancelButton);
		$(this.cancelButton).click(this.cancel);
		this.$el.append(this.form);
		$(this.form).hide();

		this.markupView = $.el.div({'class':'work-doc-render markup-view rendered-wrapper'});
		this.$el.append(this.markupView);

		this.model.on('change:rendered', this.handleRenderedChange);
	},
	handleRenderedChange: function(){
		$(this.markupView).html(this.model.get('rendered'));
		if(this.model.get('rendered').trim() == ''){
			this.edit();
		}
	},
	edit: function(){
		$(this.markupView).hide();
		$(this.form).show().find('textarea[name=markup]').val(this.model.get('markup'));
		$(this.form).show().find('textarea[name=markup]').focus();
		$('button[name="edit-work-doc-button"]').hide();
	},
	cancel: function(){
		this.showMarkupView();
	},
	showMarkupView: function(){
		$(this.form).hide();
		$(this.markupView).show();
		this.model.trigger('edit-completed');
	},
	save: function(){
		this.model.save({'markup': $(this.form).find('textarea').val() || ' '}, {
			'success':this.handleSaved,
			'error':this.handleErrorSaving
		});
	},
	handleSaved: function(){
		this.showMarkupView();
	},
	handleError: function(){
		console.log('error', arguments);
	}

/*	<div id="work-doc-editor" style="display: block;">
		<form id="work-doc-form" action="." method="post">
			<textarea id="id_markup" rows="10" placeholder="- Check out sciencesaints.com" cols="40" name="markup"></textarea>
		</form>
		<a id="formatting-help-link" href=".">formatting help</a>
		<button accesskey="s" name="work-doc-form-button" type="button" class="positive">save</button>
		<button name="work-doc-reset-button" type="button" class="negative">cancel</button>
	</div>
*/
})

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

		this.submitButton = $.el.button({'name':'submit-form-button', 'type':'submit', 'class':'btn'}, 'to-done!');
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
		this.options.model = this.model = new phlogiston.banana.CompletedItem();
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
		this.metaData.append($.el.div({'class':'update-timestamp'}, $.el.a({'href':phlogiston.urls.banana.completed_item(this.model.get('id'))}, $.timeago(this.model.get('created')))));
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
		this.collection.on('sync', this.handleReset);
	},
	handleReset: function(){
		console.log('reset', this.collection.length)
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

		this.submitButton = $.el.button({'name':'submit-form-button', 'type':'submit', 'class':'btn'}, 'thanks!');
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
		this.metaData.append($.el.div({'class':'update-timestamp'}, $.el.a({'href':transmutable.urls.banana.gratitude(this.model.get('id'))}, $.timeago(this.model.get('created')))));
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