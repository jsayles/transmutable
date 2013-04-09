from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'banana.views.index', name='index'),
	url(r'^u/$', 'banana.views.user_redirect', name='user_redirect'),
	url(r'^u/(?P<username>[^/]+)/$', 'banana.views.user', name='user'),
	url(r'^c/(?P<id>[\d]+)/$', 'banana.views.completed_item', name='completed_item'),
	url(r'^g/(?P<id>[\d]+)$', 'banana.views.gratitude', name='gratitude'),
	url(r'^a/$', 'banana.views.activity', name='activity'),

	# Mobile views
	url(r'^m/$', 'banana.mobile_views.index', name='mobile_index'),
	url(r'^m/c/$', 'banana.mobile_views.completed_items', name='mobile_completed_items'),
	url(r'^m/a/$', 'banana.mobile_views.activity', name='mobile_activity'),
)

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
