# Django settings for sistema_bomberos project.
from .settings import *


DEBUG = False
# DEBUG = False



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
    'DATE_FORMATS': ['%d/%m/%Y'],
    'DATETIME_FORMATS': ['%d/%m/%Y %H:%M'],
    'DATE_INPUT_FORMATS': ['%d/%m/%Y'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    
}


SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "apps.api.inspectors.SwaggerAutoSchema"
}
