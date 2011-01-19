from django.conf.urls.defaults import *
from django.conf import settings
 
urlpatterns = patterns('',
	(r'^$', 'apple.views.index'),
	(r'^create-account/$' , 'apple.views.create_account'),
	(r'^send-test/$' , 'apple.views.send_test'),
	(r'^email-everyone/$' , 'apple.views.email_everyone'),
)

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
