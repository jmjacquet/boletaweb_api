# -*- coding: utf-8 -*-
from django.conf.urls import  include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import login,login2,logout,volverHome

admin.autodiscover()

urlpatterns = [    
    # url(r'^login/$', login),
    # url(r'^login2/$', login2),
    # url(r'^logout/$', logout),        
    url(r'^api/v1/', include('api.urls')),   
]
                 
if settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = volverHome
handler404 = volverHome