{% load imagetags %}
{% load wikitags %}
<script>
window.pageId = {{page.id}};
window.isNamespace = {% if page.name == "SplashPage" %}true{% else %}false{% endif %};

$(document).ready(function() {
	{% if is_mobile %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.mobile_views.wiki_edit page.namespace.name page.name %}";
		});
	{% else %}
		$('button[name="edit-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_edit page.namespace.owner.username page.namespace.name page.name %}";
		});
		$('button[name="print-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_print page.namespace.owner.username page.namespace.name page.name %}";
		});
		$('button[name="history-button"]').click(function(){
			document.location.href = "{% url peach.views.wiki_history page.namespace.owner.username page.namespace.name page.name %}";
		});
		$('button[name="delete-button"]').click(function(event){
			event.preventDefault();
			if(window.isNamespace){
				var namespace = new transmutable.Namespace({ id:{{page.namespace.id}} });
				namespace.destroy({
					'success':function(){
						document.location.href = "{% url peach.views.index %}";
					},
					'error': function(){
						alert('I could not delete.');
					}
				});
			} else {
				var page = new transmutable.WikiPage({ id: {{page.id}} });
				page.destroy({
					'success':function(){
						document.location.href = "{% url peach.views.namespace page.namespace.owner.username page.namespace.name %}";
					},
					'error': function(){
						alert('I could not delete.');
					}
				})
			}
		});
	{% endif %}
});
</script>

	{% if not hide_title %}
		<ul class="breadcrumb">
			{% if request.user.is_authenticated %}
			<li>
				<a href="{% url peach.views.index %}">Notes</a> <span class="divider">/</span>
			</li>
			{% endif %}			
			<li><a href="{{page.namespace.get_absolute_url}}">{{ page.namespace.display_name }}</a> <span class="divider">/</span></li>
			<li class="active">{{ page.name }}</li>
		</ul>
	{% endif %}

	{% if request.user.is_authenticated and page.namespace.owner.username == request.user.username %}
		<div class="wiki-control-links">
		<a href="{% url peach.views.wiki_edit page.namespace.owner.username page.namespace.name page.name %}">
			<i class="icon-edit" alt="edit"></i> edit
		</a>
		{% if not is_mobile %}
			<a href="{% url peach.views.wiki_print page.namespace.owner.username page.namespace.name page.name %}" target="_new">
				<i class="icon-print" alt="print"></i> print
			</a>
			<a href="{% url peach.views.wiki_history page.namespace.owner.username page.namespace.name page.name %}">
				<i class="icon-time" alt="history"></i> history
			</a>

			<a href="#delete" role="button" data-toggle="modal"><i class="icon-trash" alt="delete"></i> delete</a>
			<div id="delete" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="deleteLabel" aria-hidden="true">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
					<h3 id="deleteLabel">Are you sure?</h3>
				</div>
				<div class="modal-body">
					{% if page.name == "SplashPage" %}
						<p>This will permanently delete this note and all of its pages.</p>
					{% else %}
						<p>This will permanently delete this page.</p>
					{% endif %}
				</div>
					<div class="modal-footer">
					<button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
					<button name="delete-button" class="btn btn-danger">Delete</button>
				</div>
			</div>

		{% endif %}
		</div> 
	{% endif %}

	{% if page.rendered %}
		<div class="rendered-wrapper">{{ page.rendered|include_constants|safe }}</div>
	{% endif %}

	{% if page.wikifile_set.all %}
	<h3>Files:</h3>
	{% endif %}
	{% for file in page.wikifile_set.all %}
		<div class="wiki-file-item">
			<a href="{{ file.file.url }}">{{ file.display_name }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
		</div>
	{% endfor %}
