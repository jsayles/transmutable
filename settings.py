import traceback
import pprint
import os

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = PROJECT_ROOT + '/media/'
TEMPLATE_DIRS = ( PROJECT_ROOT + '/templates/', )
BACKUP_ROOT = PROJECT_ROOT + '/backups/'

DYNAMIC_MEDIA_DIRS = ['resized_image', 'person_photo']

SOUTH_AUTO_FREEZE_APP = True

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Vancouver'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/admin-media/'

#AUTH_PROFILE_MODULE = "person.UserProfile"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
	'person.context_processors.person_context',
	'context_processors.site',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'south',
	'person',
	'banana',
)

from local_settings import *
