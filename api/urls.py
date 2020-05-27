# -*- coding: utf-8 -*-
from django.conf.urls import  include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import APICuotasViewSet,APIBoletasViewSet
from api.views import CuotasCreateView,CuotasUpdateView,CuotasDestroyView,CuotasListView,SuscriptoresListView
from api.views import EstudiosListView,EstudiosCreateView,EstudiosUpdateView,EstudiosDestroyView
from api.views import EstudiosPadronListView,EstudiosPadronCreateView,EstudiosPadronUpdateView,EstudiosPadronDestroyView
from api.views import BoletasListView,BoletasDestroyView,BoletasActivListView,WebLiqListView,WebLiqCtasListView
from api.views import DRICuotaActListView,DRICuotaActCreateView,DRICuotaActDestroyView,DRICuotaActUpdateView
from api.views import prueba_api
# from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token
from rest_framework import routers
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view
from rest_framework_bulk.routes import BulkRouter


schema_view = get_swagger_view(title=u'Documentación de la Web API.')
router = routers.DefaultRouter()
router.register(r'cuotas', APICuotasViewSet)
router.register(r'boletas', APIBoletasViewSet)

urlpatterns = [       
   # url(r'^token/', obtain_jwt_token, name='token_create'),    
   # url(r'^token-refresh/', refresh_jwt_token,name='token_refresh'),
   # url(r'^token-verify/', verify_jwt_token,name='token_verify'),
   
   url(r'^cuotas/list/$', CuotasListView.as_view(),name="api_cuotas_list"),
   url(r'^cuotas/create/$', CuotasCreateView.as_view(),name="api_cuotas_create"),
   url(r'^cuotas/update/$', CuotasUpdateView.as_view(),name="api_cuotas_update"),   
   url(r'^cuotas/delete/$', CuotasDestroyView.as_view(),name="api_cuotas_delete"),

   url(r'^boletas/list/$', BoletasListView.as_view(),name="api_boletas_list"),
   url(r'^boletas/delete/$', BoletasDestroyView.as_view(),name="api_boletas_delete"),

   url(r'^boletas_activ/list/$', BoletasActivListView.as_view(),name="api_boletas_activ_list"),

   
   url(r'^estudios/list/$', EstudiosListView.as_view(),name="api_estudios_list"),
   url(r'^estudios/create/$', EstudiosCreateView.as_view(),name="api_estudios_create"),
   url(r'^estudios/update/$', EstudiosUpdateView.as_view(),name="api_estudios_update"),   
   url(r'^estudios/delete/$', EstudiosDestroyView.as_view(),name="api_estudios_delete"),

   url(r'^estudios_padron/list/$', EstudiosPadronListView.as_view(),name="api_estudios_padron_list"),
   url(r'^estudios_padron/create/$', EstudiosPadronCreateView.as_view(),name="api_estudios_padron_create"),
   url(r'^estudios_padron/update/$', EstudiosPadronUpdateView.as_view(),name="api_estudios_padron_update"),
   url(r'^estudios_padron/delete/$', EstudiosPadronDestroyView.as_view(),name="api_estudios_padron_destroy"),


   url(r'^drica/list/$', DRICuotaActListView.as_view(),name="api_drica_list"),
   url(r'^drica/create/$', DRICuotaActCreateView.as_view(),name="api_drica_create"),
   url(r'^drica/update/$', DRICuotaActUpdateView.as_view(),name="api_drica_update"),   
   url(r'^drica/delete/$', DRICuotaActDestroyView.as_view(),name="api_drica_delete"),

   url(r'^web_liq/list/$', WebLiqListView.as_view(),name="api_web_liq_list"),
   url(r'^web_liq_ctas/list/$', WebLiqCtasListView.as_view(),name="api_web_liq_ctas_list"),

   url(r'^suscriptores/list/$', SuscriptoresListView.as_view(),name="api_suscriptores_list"),


   url(r'^prueba_api/$', prueba_api,name="prueba_api"),

   url('', include(router.urls)),
   url(r'^', schema_view),
   url(r'^auth/', include('rest_framework.urls')),   

]


