import os
import logging
import traceback

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = PROJECT_ROOT + '/media/'
TEMPLATE_DIRS = ( PROJECT_ROOT + '/templates/', )
BACKUP_ROOT = PROJECT_ROOT + '/backups/'

STATIC_URL = '/static/'
STATIC_ROOT = '/mnt/static/'

STATICFILES_DIRS = (PROJECT_ROOT + '/static/', )

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_REDIRECT_URL = '/u/'
SOUTH_AUTO_FREEZE_APP = True

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Los_Angeles'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

AUTH_PROFILE_MODULE = "person.UserProfile"

USE_TZ = True

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
    'dynamicresponse.middleware.api.APIMiddleware',
    'dynamicresponse.middleware.dynamicformat.DynamicFormatMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
	'django.core.context_processors.static',
    'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'person.context_processors.person_context',
	'context_processors.site',
	'context_processors.search_form',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'tastypie',
	'gunicorn',
	'south',
	'person',
	'banana',
	'apple',
	'peach',
	'phlogiston',
)

from local_settings import *
