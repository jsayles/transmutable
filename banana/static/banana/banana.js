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

banana.models.WorkDoc = Backbone.Model.extend({
	url:function(){ return '/api/work-doc/'; }
});

banana.views.NewUserTourView = Backbone.View.extend({
	className: 'new-user-tour-view',
	initialize: function(options){
		_.bindAll(this);

		this.titleRow = $.el.div(
			{'class':'row-fluid new-user-tour-title-row'}, 
			$.el.h2({'class':'span12 alert alert-info'}, 'Get Started With ' + this.options.siteName + ', Smarty Pants!')
		);
		this.$el.append(this.titleRow);

		this.congratulationsRow = $.el.div(
			{'class':'row-fluid new-user-tour-congratulations-row'}, 
			$.el.h2({'class':'span12 alert alert-info'}, 'You Are A ' + this.options.siteName + ' Nerd!'),
			$.el.p('Those three steps (intentions, manifestations, and gratitudes) are the Big Three steps for all work.')
		);
		this.$el.append(this.congratulationsRow);

		this.infoRow = $.el.div(
			{'class':'row-fluid'},
			$.el.div({'id':'infoSpan', 'class':'span12 offset1'},
				$.el.i({'class':'icon-arrow-down'}),
				$.el.div({'class':'copy'})
			)
		);
		this.$el.append(this.infoRow);

		this.showStepOne();
	},
	showStepOne: function(){
		this.$el.find('.new-user-tour-title-row').show();
		this.$el.find('.new-user-tour-congratulations-row').hide();
		this.$el.find('#infoSpan').removeClass();
		this.$el.find('.icon-arrow-down').css({'float':'left'}).show();
		this.$el.find('.copy').css({'float': 'none', 'margin-right': 'inherit'}).show();
		this.$el.find('.copy').empty().append($.el.span('Think of a specific task that you intend to do for one of your current projects and write it below.', $.el.br(), 'Examples: "- Call Steve" or "- Research Bucky Balls".'));
	},
	showStepTwo: function(){
		this.$el.find('.new-user-tour-title-row').show();
		this.$el.find('.new-user-tour-congratulations-row').hide();
		this.$el.find('#infoSpan').removeClass().addClass('span6 offset6');
		this.$el.find('.icon-arrow-down').css({'float':'left'}).show();
		this.$el.find('.copy').css({'float': 'none', 'margin-right': 'inherit'}).show();
		this.$el.find('.copy').empty().append($.el.span('Now celebrate some task you finished by writing it below.', $.el.br(), 'Examples: "Found a mentor!" or "Served my 100th client.".'));
	},
	showStepThree: function(){
		this.$el.find('.new-user-tour-title-row').show();
		this.$el.find('.new-user-tour-congratulations-row').hide();
		this.$el.find('#infoSpan').removeClass().addClass('span6 offset5');
		this.$el.find('.icon-arrow-down').css({'float':'right'}).show();
		this.$el.find('.copy').css({'float': 'right', 'margin-right': '1em'}).show();
		this.$el.find('.copy').empty().append($.el.span('Something about gratitudes.', $.el.br(), 'Examples: "- Bink!" or "- Bonk.".'));
	},
	showStepFour: function(){
		this.$el.find('.new-user-tour-title-row').hide();
		this.$el.find('.copy').hide();
		this.$el.find('.new-user-tour-congratulations-row').show();
		this.$el.find('i.icon-arrow-down').hide();
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
		this.saveButton = $.el.button({'accesskey':'s', 'name':'work-doc-save-button', 'type':'button'}, 'save'),
		this.form.append(this.saveButton);
		$(this.saveButton).click(this.save);
		this.cancelButton = $.el.button({'name':'work-doc-cancel-button', 'type':'button'}, 'cancel')
		this.form.append(this.cancelButton);
		$(this.cancelButton).click(this.cancel);
		this.$el.append(this.form);
		$(this.form).hide();

		this.markupView = $.el.div({'class':'markup-view rendered-wrapper'});
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