var peach = peach || {};
peach.views = peach.views || {};
peach.events = peach.events || {};

function nameComparator(item){
	if(item.get('name') == 'SplashPage') return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAArgh'; // Pirate constant!
	return item.get('name', '').toLowerCase();		
}

window.schema.once('populated', function(){
	window.schema.api.peach.WikiPageCollection.prototype.comparator = nameComparator;
});


peach.events.editRequested = 'edit-requested';
peach.events.editCanceled = 'edit-canceled';
peach.events.editCompleted = 'edit-completed';
peach.events.wikiPageCreated = 'wiki-page-created';
peach.events.wikiPageDestroyed = 'wiki-page-destroyed';
peach.events.wikiPageRequested = 'wiki-page-requested';

peach.views.NamespaceBreadcrumbView = Backbone.View.extend({
	className: 'namespace-breadcrumb-view breadcrumb',
	tagName: 'ul',
	initialize: function(){
		_.bindAll(this);
		this.wikiPageCrumb = null;

		this.nsCrumb = $.el.li(this.model.get('display_name'));
		this.$el.append(this.nsCrumb);
		this.publicToggleIcon = $.el.i({'class':'icon-unlock', 'title':'toggle private'});
		this.publicToggleItem = this.nsCrumb.append($.el.a(this.publicToggleIcon));
		$(this.publicToggleItem).click(this.handlePublicToggle);
		this.archiveToggleIcon = $.el.i({'class':'icon-folder-open-alt', 'title':'toggle archive'});
		this.archiveToggleItem = this.nsCrumb.append($.el.a(this.archiveToggleIcon));
		$(this.archiveToggleItem).click(this.handleArchiveToggle);
		this.updateIcons();
		this.model.on('change', this.updateIcons);
		this.model.on(peach.events.wikiPageRequested, this.handleWikiPageRequested);
		this.model.on(peach.events.wikiPageDestroyed, this.handleWikiPageDestroyed);
	},
	handleWikiPageDestroyed: function(wikiPage){
		if(!this.wikiPageCrumb) return;
		if(this.wikiPageCrumb.wikiPage == wikiPage){
			this.wikiPageCrumb.remove();
			this.wikiPageCrumb = null;
		}
	},
	handleWikiPageRequested: function(wikiPage){
		if(this.wikiPageCrumb){
			$(this.wikiPageCrumb).remove();
		}
		if(wikiPage.get('name') == 'SplashPage') return;
		this.wikiPageCrumb = $.el.li({'class':'active'}, $.el.span({'class':'divider'}, '/'), wikiPage.get('name'));
		this.$el.append(this.wikiPageCrumb);
		this.wikiPageCrumb.wikiPage = wikiPage;
	},
	handlePublicToggle: function(){
		this.model.save({'public':!this.model.get('public')});
	},
	handleArchiveToggle: function(){
		this.model.save({'archive':!this.model.get('archive')});
	},
	updateIcons: function(){
		$(this.publicToggleIcon).removeClass().addClass(this.model.get('public') ? 'icon-unlock' : 'icon-lock');
		$(this.archiveToggleIcon).removeClass().addClass(this.model.get('archive') ? 'icon-folder-close-alt' : 'icon-folder-open-alt');
	}
});

peach.views.WikiPageItemView = Backbone.View.extend({
	className: 'wiki-page-item-view',
	tagName: 'li',
	initialize: function(){
		_.bindAll(this);
		this.link = $.el.a(this.model.get('name'));
		this.$el.append(this.link);
		$(this.link).click(this.handleSelection);
		this.options.namespace.on(peach.events.wikiPageRequested, this.handleWikiPageRequested);

		this.deleteLink = $.el.i({'class':'icon-trash delete-link'});
		if(this.model.get('name') != "SplashPage"){
			this.$el.append(this.deleteLink);
			$(this.deleteLink).click(this.handleDelete);
		}
	},
	handleDelete: function(){
		this.model.destroy({
			'success':_.bind(function(wikiPage){
				this.options.namespace.trigger(peach.events.wikiPageDestroyed, wikiPage);
			}, this),
			'error': function(){
				console.log('error', arguments);
			}
		})
	},
	handleSelection: function(){
		this.options.namespace.trigger(peach.events.wikiPageRequested, this.model);
	},
	handleWikiPageRequested: function(wikiPage){
		if(wikiPage == this.model){
			this.$el.addClass('active');
		} else {
			this.$el.removeClass('active');
		}
	}
})

peach.views.NamespacePagesView = Backbone.View.extend({
	/*
	This View renders a list of nav-tabs, one for each WikiPage in the passed Namespace model.
	When a WikiPage is clicked, it emits a peach.events.wikiPageRequested event on the Namespace.
	It also shows a widget at the bottom for adding a WikiPage to the list.
	When a new WikiPage is created, it emits a peach.events.wikiPageCreated event on the Namespace.
	*/	
	className:'namespace-pages-view',
	initialize: function(){
		_.bindAll(this);
		this.selectedName = 'SplashPage';
		this.list = $.el.ul({'class':'nav nav-tabs nav-stacked'});
		this.$el.append(this.list);
		this.wikiPageItemViews = [];

		this.newWikiPageInput = $.el.input({'type':'text', 'placeholder':'new page name'});
		this.$el.append(this.newWikiPageInput);
		$(this.newWikiPageInput).keyup(this.handleNewWikiPageInputChange);
		this.collection = new window.schema.api.peach.WikiPageCollection(null, {'filters':{'namespace':this.model.get('id')}});
		this.collection.on('sync', this.handleSync);
		this.collection.fetch();
		this.collection.on('remove', this.handleRemove);
	},
	handleNewWikiPageInputChange: function(event){
		if(event.keyCode != 13) return;
		var newName = $(this.newWikiPageInput).val().trim();
		if(!newName) return;
		for(var i=0; i < this.collection.length; i++){
			if(this.collection.at(i).get('name') == newName) return;
		}
		$(this.newWikiPageInput).val('');
		var data = {
			'name':newName,
			'namespace':this.model.get('resource_uri'),
			'content':' '
		};
		this.collection.create(data,{
				'error': function(){
					console.log('error', arguments);
				}
		});
	},
	getItemView: function(wikiPage){
		for(var i=0; i < this.wikiPageItemViews.length; i++){
			if(this.wikiPageItemViews[i].model == wikiPage) return this.wikiPageItemViews[i];
		}
		return null;
	},
	addOne: function(wikiPage){
		var itemView = this.wikiPageItemViews[this.wikiPageItemViews.length] = new peach.views.WikiPageItemView({
			'model':wikiPage,
			'namespace':this.model
		})
		$(this.list).append(itemView.el);
		if(wikiPage.get('name') == this.selectedName) $(itemView.el).addClass('active');
	},
	handleRemove: function(wikiPage){
		var itemView = this.getItemView(wikiPage);
		if(!itemView) return;
		itemView.$el.remove();
	},
	handleSync: function(){
		for(var i=0; i < this.wikiPageItemViews.length; i++){
			this.wikiPageItemViews[i].remove();
		}
		this.wikiPageItemViews = [];
		for(var i=0; i < this.collection.length; i++){
			this.addOne(this.collection.at(i));
		}
	}
});

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

		this.editLink = $.el.a($.el.i({'class':'icon-edit', 'title':'edit (alt-o)', 'alt':'edit'}), 'edit');
		this.$el.append(this.editLink);
		$(this.editLink).click(this.editRequested);
		this.printLink = $.el.a(
			{'target':'_new', 'accessKey':'p', 'href':window.urlLoader.urls.peach.username_namespace_name_print(this.options.user.get('username'), this.options.namespace.get('name'), this.model.get('name'))},
			$.el.i({'class':'icon-print', 'alt':'print'}),
			'print'
		);
		this.$el.append(this.printLink);
		this.historyLink = $.el.a(
			{'href':window.urlLoader.urls.peach.username_namespace_name_history(this.options.user.get('username'), this.options.namespace.get('name'), this.model.get('name'))},
			$.el.i({'class':'icon-time', 'alt':'history'}), 
			'history'
		);
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

		this.controlsDiv = $.el.div({'class':'controls-div'});
		this.$el.append(this.controlsDiv);
		this.cancelButton = this.controlsDiv.append($.el.button({'type':'button'}, 'Cancel'));
		$(this.cancelButton).click(this.handleCancel);
		this.saveButton = this.controlsDiv.append($.el.button({'type':'button'}, 'Save'));
		$(this.saveButton).click(this.handleSave);

		this.saveAccessLink = $.el.a({'accessKey':'s'});
		this.$el.append(this.saveAccessLink);
		$(this.saveAccessLink).click(this.handleSave);

		this.cancelAccessLink = $.el.a({'accessKey':'c'});
		this.$el.append(this.cancelAccessLink);
		$(this.cancelAccessLink).click(this.handleCancel);

	},
	handleKeyUp: function(){
		this.model.set({'content':$(this.textArea).val()});
	},
	prepareForEdit: function(){
		// save the model content so that a cancellation can restore this state
		this.restoreContent = this.model.get('content');
		if(this.model.get('content') == ' '){ // TODO make it possible to save empty strings to WikiPage.content
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
		this.wikiEditControlsView = new peach.views.WikiEditControlsView({'model':this.model, 'namespace':this.options.namespace, 'user':this.options.user, 'parent':this});
		this.$el.append(this.wikiEditControlsView.el);
		this.wikiPageRenderView = new peach.views.WikiPageRenderView({'model':this.model, 'parent':this});
		this.$el.append(this.wikiPageRenderView.el);
		this.wikiPageEditForm = new peach.views.WikiPageEditForm({'model':this.model, 'parent':this})
		this.$el.append(this.wikiPageEditForm.el);
		$(this.wikiPageEditForm.el).hide();

		this.model.on(peach.events.editRequested, this.editRequested);
		this.model.on(peach.events.editCanceled, this.editCompleted);
		this.model.on(peach.events.editCompleted, this.editCompleted);

		this.editAccessLink = $.el.a({'accessKey':'o'});
		this.$el.append(this.editAccessLink);
		$(this.editAccessLink).click(this.editRequested);

		if(this.model.get('content').trim() == '') this.editRequested();
	},
	editRequested: function(){
		this.wikiPageEditForm.prepareForEdit();
		$(this.wikiPageEditForm.el).show();
		$(this.wikiPageRenderView.el).hide();
		$(this.wikiEditControlsView.el).hide();
		// The DOM isn't ready for a focus event, so wait a bit
		setTimeout(_.bind(function(){
			$(this.wikiPageEditForm.textArea).focus();
		}, this), 100);
	},
	editCompleted: function(){
		$(this.wikiPageEditForm.el).hide();
		$(this.wikiPageRenderView.el).show();
		$(this.wikiEditControlsView.el).show();
	}
});

peach.views.NamespaceEditorSwitcherView = Backbone.View.extend({
	className: 'namespace-editor-switcher-view',
	initialize: function(){
		_.bindAll(this);
		this.wikiPageEditorView = null;
		this.model.on(peach.events.wikiPageRequested, this.handleWikiPageRequested);
		this.model.on(peach.events.wikiPageDestroyed, this.handleWikiPageDestroyed);
	},
	handleWikiPageDestroyed: function(wikiPage){
		if(!this.wikiPageEditorView) return;
		if(this.wikiPageEditorView.model == wikiPage){
			this.wikiPageEditorView.remove();
			this.wikiPageEditorView = null;
		}
	},
	handleWikiPageRequested: function(wikiPage){
		if(this.wikiPageEditorView){
			this.wikiPageEditorView.remove();
		}
		this.wikiPageEditorView = new peach.views.WikiPageEditorView({
			'model':wikiPage,
			'namespace':window.namespace,
			'user':window.user
		});
		this.$el.append(this.wikiPageEditorView.el);
	}
})

