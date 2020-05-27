# -*- coding: utf-8 -*-
from .settings import *


DEBUG = True
# DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': MUNI_DB,           # Or path to database file if using sqlite3.
        'USER': DB_USER,           # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,            # Not used with sqlite3.        
        'HOST': 'localhost',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default.
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}


import sys
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING: #Covers regular testing and django-coverage
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', #
            'NAME': 'test.db', # Ruta al archivo de la base de datos
            }
        }

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',#Barra DEBUG    
# ]
# INSTALLED_APPS += [
#     "django_pdb",
#     #'debug_toolbar',        
# ]

# LOGGING = {
#     "version": 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler'
#         }
#     },
#     "loggers": {
#         "django.db.backends": {
#             'handlers': ['console'],
#             "level": "DEBUG",
#         },
#     },
# }


