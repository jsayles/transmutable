from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'banana.views.index'),
	(r'^edit/workdoc/$', 'banana.views.workdoc_edit'),
	(r'^edit/completed/$', 'banana.views.completed_edit'),
	(r'^edit/completed/rock/$', 'banana.views.rock_completed_item'),
	(r'^u/$', 'banana.views.user_redirect'),
	(r'^u/(?P<username>[^/]+)/$', 'banana.views.user'),
	(r'^u/(?P<username>[^/]+)/completed/(?P<id>[\d]+)/$', 'banana.views.completed_item'),

	(r'^m/$', 'banana.mobile_views.index'),
	(r'^m/to-done/$', 'banana.mobile_views.todone'),
	(r'^m/to-do/edit/$', 'banana.mobile_views.todo_edit'),
	(r'^m/activity/$', 'banana.mobile_views.activity'),

	(r'^test/$', 'banana.views.test'),
)

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
