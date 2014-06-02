# Django settings for youthmap project.
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


# ON_ROSTI = False
# if 'app_00290' in os.environ.get('PATH'):
ON_ROSTI = False

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

DEBUG = not ON_ROSTI
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Adrian Fedoreanu', 'phedoreanu@yahoo.com'),
)

MANAGERS = ADMINS

DATE_FORMAT = 'd/m/Y'

DATE_INPUT_FORMATS = ('%d/%m/%Y', )

if ON_ROSTI:
    APPNAME = 'app'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'my_00156',
            'USER': 'my_00156',
            'PASSWORD': 'maps2013',
            'HOST': 'store.rosti.cz',
            'PORT': '3306',
        }
    }
else:
    APPNAME = 'youth'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'youthmap',
            'USER': 'youthmap',
            'PASSWORD': 'youthmap123',
            'HOST': 'localhost',
            'PORT': '', # Set to empty string for default. Not used with sqlite3.
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'frank', 'youthmap.org', 'www.youthmap.org'
]

DEFAULT_FROM_EMAIL = 'no-reply@youthmap.org'

# Email SMTP
EMAIL_HOST = 'mail.rosti.cz'
EMAIL_PORT = '2525'
EMAIL_HOST_USER = 'activation@youthmap.org'
EMAIL_HOST_PASSWORD = 'newpassword2012'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/youthmap/media/'
if ON_ROSTI:
    MEDIA_ROOT = '/home/apps/app_00290/app/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = '/var/www/youthmap/static/'
STATIC_ROOT = '/var/www/youthmap/static/'
if ON_ROSTI:
    STATIC_ROOT = '/home/apps/app_00290/app/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
# if ON_OPENSHIFT:
STATIC_URL = '/static/'
# else:
#     STATIC_URL = 'http://localhost/youthmap/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
# os.path.join(settings.BASE_DIR, "static"),
# '/var/www/static/',
#os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j6=wswrf80xpv+bs#48i9*q@z7*z9n&v#b!(g%zny$ocqp&j15'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'youthmap.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'youthmap.wsgi.application'

# if ON_ROSTI:
#     TEMPLATE_DIRS = (
#         '/home/apps/app_00290/app/templates',
#         '/home/apps/app_00290/app/youth/templates',
#     )
# else:
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, APPNAME, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    # Uncomment the next line to enable the admin:
    'suit',
    #'suit_redactor',
    'django_select2',
    # 'suit_ckeditor',
    'django.contrib.admin',
    'crispy_forms',
    'south',
    'cities_light',
    'sorl.thumbnail',
    'djangoratings',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'youth',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'dashboard'

LOGOUT_URL = 'index'

# CRISPY_CLASS_CONVERTERS = {'textinput': 'textinput input-text'}
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#AUTO_RENDER_SELECT2_STATICS = False

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# SESSION_COOKIE_AGE = 360

TEMPLATED_EMAIL_TEMPLATE_DIR = 'youth/templated_email/' #use '' for top level template dir, ensure there is a trailing slash
# TEMPLATED_EMAIL_FILE_EXTENSION = 'email'