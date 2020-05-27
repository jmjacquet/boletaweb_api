import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)


from django.core.wsgi import get_wsgi_application


def application(environ, start_response):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'boletaweb_api.development'
  os.environ["MUNI_ID"] = environ.get("MUNI_ID", "000")
  os.environ["MUNI_DB"] = environ.get("MUNI_DB", "gg_prueba")
  os.environ["MUNI_DIR"] = environ.get("MUNI_DIR", "prueba")     
  _application = get_wsgi_application()
  return _application(environ, start_response)



