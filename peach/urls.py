# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings
 
urlpatterns = patterns('',
	(r'^$', 'peach.views.index'),
	(r'^photo/(?P<id>[\d]+)/$' , 'peach.views.photo_redirect'),
	(r'^photo-detail/(?P<id>[\d]+)/$' , 'peach.views.photo_detail_redirect'),
	(r'^m/$', 'peach.mobile_views.index'),
	(r'^m/(?P<namespace>[^/]+)/$', 'peach.mobile_views.namespace'),
	(r'^m/(?P<namespace>[^/]+)/(?P<name>[^/]+)/$', 'peach.mobile_views.wiki'),
	(r'^m/(?P<namespace>[^/]+)/(?P<name>[^/]+)/edit/$', 'peach.mobile_views.wiki_edit'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/$', 'peach.views.namespace'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/$', 'peach.views.wiki'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/history/(?P<id>[^/]+)$' , 'peach.views.wiki_page_log'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/history/$' , 'peach.views.wiki_history'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/photo/(?P<id>[\d]+)/$' , 'peach.views.photo'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/file/(?P<id>[\d]+)/$' , 'peach.views.file'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/add/$' , 'peach.views.wiki_add'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/edit/$' , 'peach.views.wiki_edit'),
	(r'^(?P<username>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/print/$' , 'peach.views.wiki_print'),
)