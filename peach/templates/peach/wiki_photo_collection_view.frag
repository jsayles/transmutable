<script>
	function showWikiPhotoDialog(imageUrl, displayName){
		var photoModalContent = $.el.div(
			$.el.img({'src':imageUrl, 'width':'1000'})
		);
		var photoModalDialog = new peach.views.ModalDialog(null, {
			'title': displayName,
			'danger': false,
			'buttons':[],
			'message': photoModalContent
		});
		photoModalDialog.goModal();
	}
</script>
<ul class="wiki-photo-collection-view">
	{% for wiki_photo in page.wiki_photos.all %}
		<li class="wiki-photo-item-view">
			<a href="." onclick="showWikiPhotoDialog('{{ wiki_photo.web_image_url }}', '{{ wiki_photo.display_name }}'); return false;">
				<img class="wiki-photo-item-image" src="{{ wiki_photo.web_thumb_url }}" />
			</a>
			<div>{{wiki_photo.display_name}}</div>
		</li>
	{% endfor %}
</ul>
