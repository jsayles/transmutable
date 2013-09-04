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
peach.events.dialogButtonPressed = 'dialog-button-pressed';

peach.views.ModalDialog = Backbone.View.extend({
	className: 'modal-dialog',
	initialize: function(attributes, options){
		/*
		this.options.title = null
		this.options.message = string or element
		this.options.buttons = [ [name,],  ]
		this.options.danger = false
		*/
		_.bindAll(this);
		this.options = options;

		this.message = $.el.div({
			'class':'modal hide fade',
			'id':'delete',
			'tabindex':'-1', 
			'role':'dialog', 
			'aria-labelledby':'deleteLabel',
			'aria-hidden':'true'
		});
		this.header = this.message.append($.el.div({'class':'modal-header'}, 
			$.el.button({'type':'button', 'data-dismiss':'modal', 'aria-hidden':'true', 'class':'close'}, 'x'),
			$.el.h3({'id':'deleteLabel'}, this.options.title)
		));
		this.body = this.message.append($.el.div({'class':'modal-body center'}, this.options.message));
		this.footer = this.message.append($.el.div({'class':'modal-footer'}));
		for(var i=0; i < this.options.buttons.length; i++){
			var buttonOptions = {
				'class':'btn',
				'data-dismiss':'modal',
				'aria-hidden':'true'
			}
			if(i == this.options.buttons.length - 1 && this.options.danger){
				buttonOptions['class'] += ' btn-danger'
			}
			var button = this.footer.append($.el.button(buttonOptions, this.options.buttons[i][0]));
			$(button).click(this.handleButtonClicked);
		}
	},
	handleButtonClicked: function(event){
		this.trigger(peach.events.dialogButtonPressed, event.target.textContent);
	},
	goModal: function(){
		$(this.message).modal('show');
	}
})

peach.views.NewNotesTourView = Backbone.View.extend({
	className: 'new-notes-tour-view',
	initialize: function(options){
		_.bindAll(this);
		this.options = options;
		this.titleRow = $.el.div(
			{'class':'row-fluid new-notes-tour-title-row'}, 
			$.el.h2({'class':'span12'}, 'Let\'s get started with notes!'),
			$.el.p('Create a note to store thoughts about a project you\'re working on.')

		);
		this.$el.append(this.titleRow);
	}
})

peach.views.NewNamespaceTourView = Backbone.View.extend({
	className: 'new-namespace-tour-view',
	initialize: function(options){
		_.bindAll(this);
		this.options = options;
		this.titleRow = $.el.div(
			{'class':'row-fluid new-namespace-tour-title-row'}, 
			$.el.h2({'class':'span12'}, 'Now add some content.'),
			$.el.p('Write up your latest, brilliant thoughts and perhaps make a list or two.')
		);
		this.$el.append(this.titleRow);

		this.collection.on(peach.events.editCompleted, this.handleEditCompleted);
		this.collection.on(peach.events.wikiPageCreated, this.handlePageCreated);
	},
	handleEditCompleted: function(){
		$(this.titleRow).empty().append($.el.h2({'class':'span12'}, 'Now, add another page over on the left.'), $.el.p('(don\'t worry, you can delete it later)'));
	},
	handlePageCreated: function(){
		$(this.titleRow).empty().append($.el.h2({'class':'span12'}, 'You did it. Keep going!'));
		setTimeout(function(){
			$('.new-namespace-tour-view').hide(400);
		}, 5000);
	}
})

peach.views.CreateNamespaceForm = Backbone.View.extend({
	className: 'create-namespace-view',
	initialize: function(options){
		_.bindAll(this);
		this.options = options;
		this.newNamespaceInput = $.el.input({'type':'text', 'placeholder':'Type a Project Name and hit Enter'});
		this.$el.append(this.newNamespaceInput);
		$(this.newNamespaceInput).keyup(this.handleInputChange);		
	},
	handleInputChange: function(event){
		if(event.keyCode != 13) return;
		var newName = $(this.newNamespaceInput).val().trim();
		if(!newName) return;
		$(this.newNamespaceInput).val('');
		var namespace = new window.schema.api.peach.Namespace({
			'display_name':newName
		});

		namespace.save(null,{
			'success':_.bind(function(model){
				if(this.options.saveCallback){
					this.options.saveCallback(model);
				}
			}, this),
			'error': _.bind(function(){
				if(this.options.saveCallback){
					this.options.saveCallback(null);
				}
			}, this)
		});
	}
})

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

		var deleteMessage = $.el.p('This will ', $.el.strong('permanently delete'), ' the ',  $.el.strong(this.model.get('display_name')), ' note and ',  $.el.strong('all of its sub-pages.'));
		this.deleteDialog = new peach.views.ModalDialog(null, {
			'title':'Are you sure?',
			'message':deleteMessage,
			'buttons':[['Cancel'], ['Delete']],
			'danger': true
		});
		this.deleteDialog.on(peach.events.dialogButtonPressed, this.handleDialogButtonPress);

		this.deleteLink = $.el.a({'href':'#delete'}, $.el.i({'class':'icon-trash', 'alt':'delete'}));
		$(this.deleteLink).click(_.bind(function(){
			this.deleteDialog.goModal();
		}, this));
		this.nsCrumb.append(this.deleteLink);

		this.updateIcons();
		this.model.on('change', this.updateIcons);
		this.model.on(peach.events.wikiPageRequested, this.handleWikiPageRequested);
		this.model.on(peach.events.wikiPageDestroyed, this.handleWikiPageDestroyed);
	},
	handleDialogButtonPress: function(buttonName){
		if(buttonName != 'Delete') return;
		this.model.destroy({
			'success': _.bind(function(){
				this.model.trigger(peach.events.namespaceDestroyed, this.model);
			}, this)
		})
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
		this.listenTo(this.options.namespace, peach.events.wikiPageRequested, this.handleWikiPageRequested);

		var deleteMessage = $.el.p('This will permanently delete this page, ', this.model.get('name'), '.');
		this.deleteDialog = new peach.views.ModalDialog(null, {
			'title':'Are you sure?',
			'message':deleteMessage,
			'buttons':[['Cancel'], ['Delete']],
			'danger': true
		});
		this.listenTo(this.deleteDialog, peach.events.dialogButtonPressed, this.handleDialogButtonPress);

		this.deleteLink = $.el.i({'class':'icon-trash delete-link'});
		$(this.deleteLink).click(_.bind(function(){
			this.deleteDialog.goModal();
		}, this));
		if(this.model.get('name') != "SplashPage"){
			this.$el.append(this.deleteLink);
		}
	},
	handleDialogButtonPress: function(buttonName){
		if(buttonName != 'Delete') return;
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
		this.collection.once('sync', this.handleSync);
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
				'success':_.bind(function(wikiPage){
					this.collection.trigger(peach.events.wikiPageCreated, wikiPage);
					setTimeout(_.bind(function(){
						namespace.trigger(peach.events.wikiPageRequested, wikiPage);
					}, {'namespace':this.model, 'wikiPage':wikiPage}), 500);
				}, this),
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
		this.wikiPageItemViews = _.without(this.wikiPageItemViews, itemView);
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
		this.collection.on('add', this.addOne);
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
		$(this.editLink).click(this.editRequested);
		this.printLink = $.el.a(
			{'target':'_new', 'accessKey':'p', 'href':window.urlLoader.urls.peach.username_namespace_name_print(this.options.user.get('username'), this.options.namespace.get('name'), this.model.get('name'))},
			$.el.i({'class':'icon-print', 'alt':'print'}),
			'print'
		);
		this.historyLink = $.el.a(
			{'href':window.urlLoader.urls.peach.username_namespace_name_history(this.options.user.get('username'), this.options.namespace.get('name'), this.model.get('name'))},
			$.el.i({'class':'icon-time', 'alt':'history'}), 
			'history'
		);

		this.$el.append(this.editLink);
		if(!this.options.isMobile){
			this.$el.append(this.printLink);
			this.$el.append(this.historyLink);
		}
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

		this.textArea = this.form.append($.el.textarea({'placeholder':'Here are a few thoughts on my project...'}));
		$(this.textArea).keyup(this.handleKeyUp);

		this.controlsDiv = $.el.div({'class':'controls-div'});
		this.$el.append(this.controlsDiv);

		this.markdownLink = $.el.a({'href':'http://daringfireball.net/projects/markdown/syntax', 'target':'_new'}, 'Formatting');
		this.controlsDiv.append(this.markdownLink);

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
		this.model.trigger(peach.events.editCompleted, this.model);
	}
})

peach.views.makeFileDrop = function(targetEl, filesCallback){
	var el = $(targetEl);
	el.addClass('file-drop');
	el.on('dragover', function(e) { e.preventDefault(); e.stopPropagation(); } );
	el.on('dragenter', function(e) { e.preventDefault(); e.stopPropagation(); } );
	el.on('drop',
		_.bind(function(e){
			if(!e.originalEvent.dataTransfer) return;
			if(e.originalEvent.dataTransfer.files.length <= 0) return;
			e.preventDefault();
			e.stopPropagation();
			filesCallback(e.originalEvent.dataTransfer.files);
		}, this)
	);
}

peach.views.WikiPhotoEditItemView = Backbone.View.extend({
	tagName: 'li',
	className:'wiki-photo-item-view',
	initialize: function(){
		_.bindAll(this);
		var deleteIcon = $.el.a({'class':'delete-link', 'href':'#delete'}, $.el.i({'class':'icon-trash'}));
		this.$el.append(deleteIcon);
		this.$el.append($.el.a({'href':this.model.get('web_image'), 'target':'_new'}, $.el.img({'src':this.model.get('web_thumb')})));
		this.$el.append($.el.div(this.model.get('display_name')));

		var deleteMessage = $.el.p('This will permanently delete this image, ', this.model.get('display_name'), '.');
		this.deleteDialog = new peach.views.ModalDialog(null, {
			'title':'Are you sure?',
			'message':deleteMessage,
			'buttons':[['Cancel'], ['Delete']],
			'danger': true
		});
		this.listenTo(this.deleteDialog, peach.events.dialogButtonPressed, this.handleDeleteDialog);
		$(deleteIcon).click(this.deleteDialog.goModal);
	},
	showDeleteDialog: function(event){
		event.preventDefault();
		event.stopPropagation();
	},
	handleDeleteDialog: function(buttonName){
		if(buttonName != 'Delete') return;
		this.model.destroy({
			'success':this.handleDestroySuccess,
			'error':this.handleDestoryError
		});
	},
	handleDestroySuccess: function(){
		//pass
	},
	handleDestoryError: function(){
		console.log('Error', arguments);
	}
});

peach.views.WikiPhotoItemView = Backbone.View.extend({
	tagName: 'div',
	className:'wiki-photo-item-view',
	initialize: function(){
		_.bindAll(this);
		var image = $.el.img({'class':'wiki-photo-item-img', 'src':this.model.get('web_thumb')});
		this.$el.append(image);
		$(image).click(this.handleImageClick);
		this.$el.append($.el.div(this.model.get('display_name')));

		this.photoModalContent = $.el.div(
			$.el.img({'src':this.model.get('web_image'), 'width':'1000'}),
			$.el.a({'href':this.model.get('image'), 'target':'_new'}, 'original')
		);
		this.photoModalDialog = new peach.views.ModalDialog(null, {
			'title': this.model.get('display_name'),
			'danger': false,
			'buttons':[['Close']],
			'message': this.photoModalContent
		});
	},
	handleImageClick: function(){
		this.photoModalDialog.goModal();
	}
});

peach.views.WikiPhotosEditorView = Backbone.View.extend({
	className: 'wiki-page-file-editor-view',
	initialize: function(){
		_.bindAll(this);

		this.wikiPhotoCollectionView = new transmutable.views.GenericCollectionView({
			'collection': this.options.collection,
			'itemClass':peach.views.WikiPhotoEditItemView
		});
		this.wikiPhotoCollectionView.$el.addClass('wiki-photo-collection-view');
		this.$el.append(this.wikiPhotoCollectionView.el);

		this.addImageGraphic = $.el.div(
			$.el.i({'class':'icon-plus', 'title':'add or drop image'}), 
			' ',
			$.el.i({'class':'icon-picture', 'title':'add or drop image'})
		)
		this.spinner = $.el.i({'class':'icon-spinner icon-spin'});
		this.addImageLink = $.el.a({'href':'#', 'alt':'add or drop image'},
			this.addImageGraphic,
			this.spinner
		);
		this.$el.append(this.addImageLink);
		$(this.spinner).hide();
		$(this.addImageLink).click(this.handleAddImageClick);
		peach.views.makeFileDrop(this.addImageLink, this.handleFiles);

		// A hidden form whose file dialog is shown when the addImageLink is clicked
        var form = $.el.form({'class':'file-form', 'action':'.', 'method':'post', 'enctype':'multipart-form-data'});
        this.$el.append(form);
        var input = form.append($.el.input({'type':'file', 'accept':'image/png,image/jpeg,image/gif,image/tiff'}));
        $(input).change(this.handleFileInputChange);
	},
	handleAddImageClick: function(event){
		event.preventDefault();
		event.stopPropagation();
        this.$el.find('.file-form input').click();
	},
	handleFileInputChange: function(event){ this.handleFiles(event.target.files); },
	handleFiles: function(files){
		var data = {
			'upload_photos_action':true
		};
		for(var i=0; i < files.length; i++){
			data[files[i].name] = files[i];
		}
		$(this.addImageGraphic).hide();
		$(this.spinner).show();
		new transmutable.MultipartUploader(data, this.handleUploaderProgress, this.model.get('public_url'));
	},
	handleUploaderProgress: function(uploader, progress){
		if(progress == 100 || progress == -1){
			$(this.spinner).hide();
			$(this.addImageGraphic).show();
		}
		if(progress == -1){ // error
			console.log("Error uploading");
		} else if(progress == 100){ // success
			var newPhotos = JSON.parse(uploader.xhr.response);
			for(var i=0; i < newPhotos.length; i++){
				this.options.collection.add(new window.schema.api.peach.WikiPhoto(newPhotos[i]));
			}
		}
	}
})

peach.views.WikiPageEditorView = Backbone.View.extend({
	className: 'wiki-page-editor-view container',
	initialize: function(){
		_.bindAll(this);
		this.photoCollection = new window.schema.api.peach.WikiPhotoCollection();

		var row = $.el.div({'class':'row-fluid'});
		this.$el.append(row);

		this.wikiPageRenderView = new peach.views.WikiPageRenderView({
			'model':this.model,
			'user':this.options.user,
			'isMobile':this.options.isMobile,
			'namespace':this.options.namespace, 
			'photoCollection':this.photoCollection
		});
		this.wikiPageRenderView.$el.addClass('span9')
		row.append(this.wikiPageRenderView.el);

		this.leftRenderColumn = $.el.div({'class':'span3'});
		row.append(this.leftRenderColumn);

		this.wikiEditControlsView = new peach.views.WikiEditControlsView({
			'model':this.model, 
			'user':this.options.user, 
			'namespace':this.options.namespace, 
			'isMobile':this.options.isMobile
		});
		this.leftRenderColumn.append(this.wikiEditControlsView.el);

		this.wikiPhotoCollectionView = new transmutable.views.GenericCollectionView({
			'collection': this.photoCollection,
			'itemClass':peach.views.WikiPhotoItemView
		});
		this.wikiPhotoCollectionView.$el.addClass('wiki-photo-collection-view');
		this.leftRenderColumn.append(this.wikiPhotoCollectionView.el);

		this.wikiPageEditForm = new peach.views.WikiPageEditForm({
			'model':this.model,
			'isMobile':this.options.isMobile
		})
		this.wikiPageEditForm.$el.addClass('span9')
		row.append(this.wikiPageEditForm.el);
		$(this.wikiPageEditForm.el).hide();

		this.wikiPhotosEditorView = new peach.views.WikiPhotosEditorView({
			'model':this.model,
			'collection':this.photoCollection,
			'isMobile':this.options.isMobile
		})
		this.wikiPhotosEditorView.$el.addClass('span3')
		row.append(this.wikiPhotosEditorView.el);
		$(this.wikiPhotosEditorView.el).hide();

		this.model.on(peach.events.editRequested, this.editRequested);
		this.model.on(peach.events.editCanceled, this.editCompleted);
		this.model.on(peach.events.editCompleted, this.editCompleted);

		this.editAccessLink = $.el.a({'accessKey':'o'});
		this.$el.append(this.editAccessLink);
		$(this.editAccessLink).click(this.editRequested);

		this.photoCollection.reset(this.model.get('wiki_photos'));
		if(this.model.get('content').trim() == '') this.editRequested();
	},
	editRequested: function(){
		this.wikiPageEditForm.prepareForEdit();
		this.wikiPageEditForm.$el.show();
		this.wikiPhotosEditorView.$el.show();
		this.wikiPageRenderView.$el.hide();
		$(this.leftRenderColumn).hide();
		// The DOM isn't ready for a focus event, so wait a bit
		setTimeout(_.bind(function(){
			$(this.wikiPageEditForm.textArea).focus();
		}, this), 100);
	},
	editCompleted: function(){
		this.wikiPageEditForm.$el.hide();
		this.wikiPhotosEditorView.$el.hide();
		this.wikiPageRenderView.$el.show();
		$(this.leftRenderColumn).show();
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
			// The page removed is the currently edited page, so remove that and switch to the splash page
			this.wikiPageEditorView.remove();
			this.wikiPageEditorView = null;
			this.model.trigger(peach.events.wikiPageRequested, this.collection.at(0));
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

