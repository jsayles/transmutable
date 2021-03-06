import os
import Image
import urllib
import datetime, calendar
import random
import time
import re
import unicodedata
import traceback
import logging
import pprint
from re import sub

from django.db import models
from django.utils.html import strip_tags,  linebreaks, urlize
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.markup.templatetags.markup import markdown

from person import sanitizeHtml

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
