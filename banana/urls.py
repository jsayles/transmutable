from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'banana.views.index', name='index'),
	url(r'^u/$', 'banana.views.user_redirect', name='user_redirect'),
	url(r'^u/(?P<username>[^/]+)/$', 'banana.views.user', name='user'),
	url(r'^c/(?P<id>[\d]+)/$', 'banana.views.completed_item', name='completed_item'),
	url(r'^g/(?P<id>[\d]+)$', 'banana.views.gratitude', name='gratitude'),

	# Mobile views
	url(r'^m/$', 'banana.mobile_views.index', name='mobile_index'),
	url(r'^m/to-done/$', 'banana.mobile_views.todone', name='mobile_todone'),
	url(r'^m/to-do/edit/$', 'banana.mobile_views.todo_edit', name='mobile_todo_edit'),
	url(r'^m/activity/$', 'banana.mobile_views.activity', name='mobile_activity'),

	# API views
	url(r'^api/workdoc/$', 'banana.views.workdoc_edit', name='workdoc_edit'),
	url(r'^api/completed-item/$', 'banana.views.completed_items', name='completed_items'),
	url(r'^api/completed-item/rock$', 'banana.views.completed_item_rock', name='completed_item_rock'),
	url(r'^api/gratitude/$', 'banana.views.gratitudes', name='gratitudes'),

	# Test views
	url(r'^test/$', 'banana.views.test', name='test'),
)

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
