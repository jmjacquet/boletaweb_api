# -*- coding: utf-8 -*-
# Django settings for sistema_bomberos project.
from decouple import config
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True

ADMINS = (
       ('JuanMa', 'errores_web@grupoguadalupe.com.ar'),
)

MANAGERS = ADMINS

#Traigo los datos de configuracion del Apache

MUNI_ID = os.environ['MUNI_ID']
MUNI_DB = os.environ['MUNI_DB']
MUNI_DIR = os.environ['MUNI_DIR']
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MUNI_DB,           # Or path to database file if using sqlite3.
        'USER': DB_USER,           # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,            # Not used with sqlite3.
        'HOST': DB_HOST,                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default.
    },
}

ALLOWED_HOSTS = ['*']


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',       
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',    
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'django.contrib.humanize',
    'bootstrap3',
    'django_extensions',
    'api',
    'rest_framework',
    'rest_framework.authtoken',        
    'rest_framework_swagger',
    'corsheaders',
    
]

ROOT_URLCONF = 'boletaweb_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates') ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug' : DEBUG,
        },
    },
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),   
]


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'boletaweb_api.wsgi.application'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

LANGUAGE_CODE = 'es-AR'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
TIME_INPUT_FORMATS = ['%H:%M']
DATE_INPUT_FORMATS = ['%d/%m/%Y',]
DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M',]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_ROOT = '/home/grupogua/webapps/boletadjango/boletaWeb/media'

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DIR_MUNIS = os.path.join(STATIC_URL,'munis',MUNI_DIR)

ADMIN_MEDIA_PREFIX = os.path.join(BASE_DIR, 'static/admin/')


EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')

SERVER_EMAIL = config('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME')
SECRET_KEY = config('SECRET_KEY')

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400
LOGGING = {
   'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, "errores.log"),
            'formatter': 'verbose'
        },
         'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
            'formatter': 'verbose',
        },
          'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        'api': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

ROOT_URL = '/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
AUTH_PROFILE_MODULE = 'api.UserProfile'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
INTERNAL_IPS = ('127.0.0.1',)


CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DATE_FORMAT':  '%d/%m/%Y',
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S',        
    'DATE_INPUT_FORMATS' : ['%d/%m/%Y'],    
    
}


SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "apps.api.inspectors.SwaggerAutoSchema"
}


# REST_USE_JWT = True

# import datetime
# # JWT settings
# JWT_AUTH = {
#     'JWT_ENCODE_HANDLER':
#     'rest_framework_jwt.utils.jwt_encode_handler',
 
#     'JWT_DECODE_HANDLER':
#     'rest_framework_jwt.utils.jwt_decode_handler',
 
#     'JWT_PAYLOAD_HANDLER':
#     'rest_framework_jwt.utils.jwt_payload_handler',
 
#     'JWT_PAYLOAD_GET_USER_ID_HANDLER':
#     'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
 
#     'JWT_RESPONSE_PAYLOAD_HANDLER':
#     'rest_framework_jwt.utils.jwt_response_payload_handler',
 
#     'JWT_SECRET_KEY': SECRET_KEY,
#     'JWT_GET_USER_SECRET_KEY': None,
#     'JWT_PUBLIC_KEY': None,
#     'JWT_PRIVATE_KEY': None,
#     'JWT_ALGORITHM': 'HS256',
#     'JWT_VERIFY': True,
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_LEEWAY': 0,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
#     'JWT_AUDIENCE': None,
#     'JWT_ISSUER': None, 
#     'JWT_ALLOW_REFRESH': False,
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'GG',
#     'JWT_AUTH_COOKIE': None,
# }

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}



