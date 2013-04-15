# app lives in a directory above our example
# project so we need to make sure it is findable on our path.

import sys
from os.path import abspath, dirname, join
from os import pardir

PROJECT_DIR = abspath(dirname(__file__))
grandparent = abspath(join(PROJECT_DIR, pardir))
for path in (grandparent, PROJECT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_DIR, 'local.db'),
    }
}

ALLOWED_HOSTS = []
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = ')m%q23e1*23pgcij6-44rpgpz)i63%z7=h7!!tr0v_@01e3)c5'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'zendesk_auth',
)

#ZENDESK_URL = "https://domain.zendesk.com"
#ZENDESK_TOKEN = "my-random-token-provided-by-zendesk"
ZENDESK_URL = "https://imtapps.zendesk.com"
ZENDESK_TOKEN = "iKMa4PdCUfxDDoqHxKFlhoG88DGEXshGMDXnS4FrcKW5zY6u"
LOGIN_URL = "/admin"