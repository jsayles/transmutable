var peach = peach || {};
peach.views = peach.views || {};
peach.events = peach.events || {};

peach.events.editRequested = 'edit-requested';
peach.events.editCanceled = 'edit-canceled';
peach.events.editCompleted = 'edit-completed';

peach.views.WikiPageRenderView = Backbone.View.extend({
	className: 'wiki-page-render-view',
	initialize: function(){
		_.bindAll(this);
		this.markdownConverter = new Markdown.Converter();
		this.renderedEl = $.el.div({'class':'markup-view rendered-wrapper'});
		this.$el.append(this.renderedEl);
		this.renderContent();
		this.model.on('change:content', this.renderContent);
	},
	renderContent: function(){
		// Will this be too slow for large documents?
		$(this.renderedEl).html(this.markdownConverter.makeHtml(this.model.get('content')));
		return this;
	}
});

peach.views.WikiEditControlsView = Backbone.View.extend({
	className: 'wiki-edit-controls-view',
	initialize: function(){
		_.bindAll(this);

		this.editLink = $.el.a({'href':'#edit'}, $.el.i({'class':'icon-edit', 'alt':'edit'}), 'edit');
		this.$el.append(this.editLink);
		$(this.editLink).click(this.editRequested);
		this.printLink = $.el.a({'href':'#print'}, $.el.i({'class':'icon-print', 'alt':'print'}), 'print');
		this.$el.append(this.printLink);
		this.historyLink = $.el.a({'href':'#history'}, $.el.i({'class':'icon-time', 'alt':'history'}), 'history');
		this.$el.append(this.historyLink);
		this.deleteLink = $.el.a({'href':'#delete'}, $.el.i({'class':'icon-trash', 'alt':'delete'}), 'delete');
		this.$el.append(this.deleteLink);
	},
	editRequested: function(){
		this.model.trigger(peach.events.editRequested);
	}
})

peach.views.WikiPageEditForm = Backbone.View.extend({
	className:'wiki-page-edit-form',
	initialize: function(){
		_.bindAll(this);
		this.form = $.el.form({'action':'.', 'method':'put'});
		this.$el.append(this.form);

		this.textArea = this.form.append($.el.textarea());
		$(this.textArea).keyup(this.handleKeyUp);
		this.saveButton = this.form.append($.el.button({'type':'button'}, 'Save'));
		$(this.saveButton).click(this.handleSave);
		this.cancelButton = this.form.append($.el.button({'type':'button'}, 'Cancel'));
		$(this.cancelButton).click(this.handleCancel);
	},
	handleKeyUp: function(){
		this.model.set({'content':$(this.textArea).val()});
	},
	prepareForEdit: function(){
		// save the model content so that a cancellation can restore this state
		this.restoreContent = this.model.get('content');
		if(this.model.get('content') == ' '){
			$(this.textArea).val('');
		} else {
			$(this.textArea).val(this.model.get('content'));
		}
	},
	handleCancel: function(){
		this.model.set('content', this.restoreContent);
		this.model.trigger(peach.events.editCanceled);
	},
	handleSave: function(){
		if(this.model.get('content') == '') this.model.set({'content':' '})
		this.model.save(null, {
			'success': this.handleSaveSuccess,
			'error': this.handleSaveError
		});
	},
	handleSaveError: function(){
		console.log("Error", arguments);
	},
	handleSaveSuccess: function(){
		this.model.trigger(peach.events.editCompleted);
	}
})

peach.views.WikiPageEditorView = Backbone.View.extend({
	className: 'wiki-page-editor-view',
	initialize: function(){
		_.bindAll(this);
		this.wikiEditControlsView = new peach.views.WikiEditControlsView({'model':this.model, 'parent':this});
		this.$el.append(this.wikiEditControlsView.el);
		this.wikiPageRenderView = new peach.views.WikiPageRenderView({'model':this.model, 'parent':this});
		this.$el.append(this.wikiPageRenderView.el);
		this.wikiPageEditForm = new peach.views.WikiPageEditForm({'model':this.model, 'parent':this})
		this.$el.append(this.wikiPageEditForm.el);
		$(this.wikiPageEditForm.el).hide();

		this.model.on(peach.events.editRequested, this.editRequested);
		this.model.on(peach.events.editCanceled, this.editCompleted);
		this.model.on(peach.events.editCompleted, this.editCompleted);
	},
	editRequested: function(){
		this.wikiPageEditForm.prepareForEdit();
		$(this.wikiPageEditForm.el).show();
		$(this.wikiPageRenderView.el).hide();
		$(this.wikiEditControlsView.el).hide();
	},
	editCompleted: function(){
		$(this.wikiPageEditForm.el).hide();
		$(this.wikiPageRenderView.el).show();
		$(this.wikiEditControlsView.el).show();
	}
});



