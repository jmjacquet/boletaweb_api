# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from api.serializers import CuotasSerializer,BoletasSerializer,EstudiosSerializer,EstudioPadronSerializer,SuscriptoresSerializer
from api.serializers import Boletas_ActividadesSerializer,DRICuotaActivCuotasSerializer,WebLiqSerializer,WebLiqCtasSerializer,CuotaSerializer
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from api.models import Cuotas,Tributo,Configuracion,DriBoleta,DriBoleta_actividades,Suscriptores
from api.models import DriEstudio,DriEstudioPadron,DriCuotaActividad,WEB_Liquidacion,WEB_Liquidacion_ctas
from django.db.models import Count,Sum,F
import json
from decimal import Decimal
import decimal
from rest_framework import viewsets,mixins,generics
from rest_framework.decorators import detail_route, list_route,api_view
from rest_framework import filters,status
from django.db import connection,transaction
from rest_framework.exceptions import ValidationError
from rest_framework_bulk import BulkCreateAPIView,BulkUpdateAPIView,BulkDestroyAPIView
from api.utilidades import response_data



@api_view(['GET', 'POST','PUT'])
def prueba_api(request):
    id_cuotas,news,changes,dels,errores=[],[],[],[],[]
    response_data["success"]=False
    response_data["message"]=None
    response_data["debug"]=errores
    response_data["cantidad"]=0
    response_data["queries"]=""
    response_data["detalle"]=[{'news':news,'changes':changes,'dels':dels}]
    response_data["id_cuotas"]=id_cuotas 
    rta = request.data.copy()
    datos = rta.get("data")            
    for d in datos:            
        accion = d.get("accion")
        idc = d['id_cuota']        
        try:                            
            serializer=CuotaSerializer(data=d)
            serializer.is_valid(raise_exception=True)
            if accion=='I':
                serializer.save()
                news.append(idc)
            elif accion=='U':
                cuota = Cuotas.objects.filter(id_cuota=idc).first()                               
                if not cuota:
                    serializer.save()
                    news.append(idc)
                else:
                    serializer= CuotaSerializer(cuota,data=d)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    changes.append(idc)
            elif accion=='D':
                cuotas = Cuotas.objects.filter(id_cuota=idc).delete()
                dels.append(idc)
            id_cuotas.append(idc)
        except Exception as ee:
            errores.append({idc,str(ee)})
    try:        
        response_data["success"]=True
        response_data["message"]="%s Cuota(s)" % len(datos)
        response_data["cantidad"]=len(datos)
        response_data["status"]=status.HTTP_200_OK
        response_data["detalle"]=[{'news':news,'changes':changes,'dels':dels}]
        response_data["id_cuotas"]=id_cuotas
        response_data["debug"]=errores
        response_data["queries"]="Cantidad de Queries:%s" % len(connection.queries)   
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:        
        response_data["message"]= str(e)
    response_data["debug"]=errores
    response_data["queries"]="Cantidad de Queries:%s" % len(connection.queries)   
    response_data["detalle"]=[{'news':news,'changes':changes,'dels':dels}]
    response_data["id_cuotas"]=id_cuotas
    response_data["status"]=status.HTTP_400_BAD_REQUEST                
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)





################################ CUOTAS GET/POST/PUT/DELETE ############################
class CuotasListView(generics.ListAPIView):    
    serializer_class = CuotasSerializer    
    queryset = Cuotas.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(CuotasListView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        cuotas = self.get_queryset()        
        try:
            tributo =self.request.query_params.get('tributo', None) 
            if tributo:
                    cuotas = cuotas.filter(tributo=tributo)
        except:
            pass
        try:
            id_unidad =self.request.query_params.get('id_unidad', None) 
            if id_unidad:
                    cuotas = cuotas.filter(id_unidad=id_unidad)
        except:
            pass
        try:
            anio_desde =self.request.query_params.get('anio_desde', None) 
            if anio_desde:
                    cuotas = cuotas.filter(anio__gte=anio_desde)
        except:
            pass
        try:
            anio_hasta =self.request.query_params.get('anio_hasta', None) 
            if anio_hasta:
                    cuotas = cuotas.filter(anio__lte=anio_hasta)
        except:
            pass
        cant=len(cuotas)
        serializer = CuotasSerializer(cuotas, many=True)
        return Response({'data':serializer.data,'cantidad':cant})


class CuotasCreateView(BulkCreateAPIView):
    queryset = Cuotas.objects.all()
    serializer_class = CuotasSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(CuotasCreateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def create(self, request, *args, **kwargs):
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)        
        if serializer.is_valid():
            vd = serializer.validated_data                        
            try:
                with transaction.atomic():
                    self.perform_create(serializer)       
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.validated_data)

            response_data["success"]=True
            response_data["message"]="%s Cuota(s) Agregada(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_201_CREATED
            response_data["detalle"] = [v['id_cuota'] for v in vd]
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class CuotasUpdateView(BulkUpdateAPIView):
    queryset = Cuotas.objects.all()
    serializer_class = CuotasSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(CuotasUpdateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries
        return response


    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data                                    
            try:
                with transaction.atomic():
                    self.perform_bulk_update(serializer)           
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)          

            response_data["success"]=True
            response_data["message"]="%s Cuota(s) Actualizada(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_200_OK
            response_data["detalle"] = [v['id_cuota'] for v in vd]
            
            return Response(response_data, status=status.HTTP_200_OK)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)        

class CuotasDestroyView(generics.GenericAPIView):        
    permission_classes = (AllowAny,)
    serializer_class = CuotasSerializer
    

    def dispatch(self, request, *args, **kwargs):
        response = super(CuotasDestroyView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def delete(self, request, *args, **kwargs):
        id_cuotas = []
        cuotas = None
        cant = 0
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=cant
        response_data["detalle"]=id_cuotas
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)      
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                id_cuotas = [v['id_cuota'] for v in vd]
                with transaction.atomic():                    
                    cuotas = Cuotas.objects.filter(id_cuota__in=id_cuotas)
                    cant = cuotas.count()                   
                    cuotas = cuotas.delete()
            except Exception as e:
                response_data["debug"]=str(e)
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data["detalle"] = id_cuotas            
            response_data["success"]=True
            response_data["message"]="%s Cuota(s) Eliminada(s)" % cant
            response_data["cantidad"]=cant
            response_data["debug"]= str(cuotas)
            response_data["status"]=status.HTTP_201_CREATED
            
            
            return Response(response_data, status=status.HTTP_201_CREATED)
       
        response_data["message"]= str(serializer.errors)
        response_data["debug"]=str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    

################################ BOLETAS GET ############################

class BoletasListView(generics.ListAPIView):        
    serializer_class = BoletasSerializer
    queryset = DriBoleta.objects.all().prefetch_related('boleta_actividad',)       
    permission_classes = (AllowAny,)
    

    def dispatch(self, request, *args, **kwargs):
        response = super(BoletasListView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def list(self,*args, **kwargs):
        boletas = self.get_queryset()
        try:
            id_boleta =self.request.query_params.get('id_boleta', None) 
            if id_boleta:
                    boletas = boletas.filter(id_boleta=id_boleta)
        except:
            pass
        try:
            id_padron =self.request.query_params.get('id_padron', None) 
            if id_padron:
                    boletas = boletas.filter(id_padron=id_padron)
        except:
            pass
        try:
            id_cuota =self.request.query_params.get('id_cuota', None) 
            if id_cuota:
                    cuotas = cuotas.filter(id_cuota__pk=id_cuota)
        except:
            pass
        try:
            anio_desde =self.request.query_params.get('anio_desde', None) 
            if anio_desde:
                    boletas = boletas.filter(anio__gte=anio_desde)
        except:
            pass
        try:
            anio_hasta =self.request.query_params.get('anio_hasta', None) 
            if anio_hasta:
                    boletas = boletas.filter(anio__lte=anio_hasta)
        except:
            pass
        cant=len(boletas)
        serializer = BoletasSerializer(boletas, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class BoletasActivListView(generics.ListAPIView):        
    serializer_class = Boletas_ActividadesSerializer
    queryset = DriBoleta_actividades.objects.all()
    permission_classes = (AllowAny,)
    

    def dispatch(self, request, *args, **kwargs):
        response = super(BoletasActivListView, self).dispatch(request, *args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def list(self,*args, **kwargs):
        boletas = self.get_queryset()
        print self.request.query_params
        try:
            id_boleta =self.request.query_params.get('id_boleta', None) 
            if id_boleta:
                    boletas = boletas.filter(id_boleta=id_boleta)
        except:
            pass
        try:
            id_actividad =self.request.query_params.get('id_actividad', None) 
            if id_actividad:
                    cuotas = cuotas.filter(id_actividad=id_actividad)       
        except:
            pass
        cant=len(boletas)
        serializer = Boletas_ActividadesSerializer(boletas, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class BoletasDestroyView(generics.GenericAPIView):        
    permission_classes = (AllowAny,)
    serializer_class = BoletasSerializer
    

    def dispatch(self, request, *args, **kwargs):
        response = super(BoletasDestroyView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def delete(self, request, *args, **kwargs):
        id_boletas = []
        boletas = None
        cant = 0
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=cant
        response_data["detalle"]=id_boletas
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)      
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                id_boletas = [v['id_boleta'] for v in vd]
                with transaction.atomic():                    
                    boletas = DriBoleta.objects.filter(id_boleta__in=id_boletas)
                    cant = boletas.count()                   
                    cuotas = boletas.delete()
            except Exception as e:
                response_data["debug"]=str(e)
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data["detalle"] = id_boletas            
            response_data["success"]=True
            response_data["message"]="%s Boletas(s) Eliminada(s)" % cant
            response_data["cantidad"]=cant
            response_data["debug"]= str(boletas)
            response_data["status"]=status.HTTP_201_CREATED
            
            
            return Response(response_data, status=status.HTTP_201_CREATED)
       
        response_data["message"]= str(serializer.errors)
        response_data["debug"]=str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


################################ ESTUDIOS GET/POST/PUT/DELETE ############################

class EstudiosListView(generics.ListAPIView):    
    serializer_class = EstudiosSerializer    
    queryset = DriEstudio.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        estudios = self.get_queryset()
        print self.request.query_params
        try:
            tributo =self.request.query_params.get('tributo', None) 
            if tributo:
                    estudios = estudios.filter(tributo=tributo)
        except:
            pass
        try:
            id_unidad =self.request.query_params.get('id_unidad', None) 
            if id_unidad:
                    estudios = estudios.filter(id_unidad=id_unidad)
        except:
            pass
        try:
            anio_desde =self.request.query_params.get('anio_desde', None) 
            if anio_desde:
                    estudios = estudios.filter(anio__gte=anio_desde)
        except:
            pass
        try:
            anio_hasta =self.request.query_params.get('anio_hasta', None) 
            if anio_hasta:
                    estudios = estudios.filter(anio__lte=anio_hasta)
        except:
            pass
        cant=len(estudios)
        serializer = EstudiosSerializer(estudios, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class EstudiosCreateView(BulkCreateAPIView):
    queryset = DriEstudio.objects.all()
    serializer_class = EstudiosSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosCreateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def create(self, request, *args, **kwargs):
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)        
        if serializer.is_valid():
            vd = serializer.validated_data                        
            try:
                with transaction.atomic():
                    self.perform_create(serializer)       
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.validated_data)

            response_data["success"]=True
            response_data["message"]="%s Estudio(s) Agregado(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_201_CREATED
            response_data["detalle"] = [v['id_estudioc'] for v in vd]
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class EstudiosUpdateView(BulkUpdateAPIView):
    queryset = DriEstudio.objects.all()
    serializer_class = EstudiosSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosUpdateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries
        return response


    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data                                    
            try:
                with transaction.atomic():
                    self.perform_bulk_update(serializer)           
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)          

            response_data["success"]=True
            response_data["message"]="%s Estudio(s) Actualizado(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_200_OK
            response_data["detalle"] = [v['id_estudioc'] for v in vd]
            
            return Response(response_data, status=status.HTTP_200_OK)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)        

class EstudiosDestroyView(generics.GenericAPIView):        
    permission_classes = (AllowAny,)
    serializer_class = EstudiosSerializer
    

    def dispatch(self, request, *args, **kwargs):
        response = super(EstudiosDestroyView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def delete(self, request, *args, **kwargs):
        id_estudios = []
        estudios = None
        cant = 0
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=cant
        response_data["detalle"]=id_estudios
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)      
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                id_estudios = [v['id_estudioc'] for v in vd]
                with transaction.atomic():                    
                    estudios = DriEstudio.objects.filter(id_estudioc__in=id_estudios)
                    cant = estudios.count()                   
                    estudios = estudios.delete()
            except Exception as e:
                response_data["debug"]=str(e)
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data["detalle"] = id_estudios            
            response_data["success"]=True
            response_data["message"]="%s Estudios Padron(es) Eliminado(s)" % cant
            response_data["cantidad"]=cant
            response_data["debug"]= str(estudios)
            response_data["status"]=status.HTTP_201_CREATED
            return Response(response_data, status=status.HTTP_201_CREATED)
       
        response_data["message"]= str(serializer.errors)
        response_data["debug"]=str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class EstudiosPadronListView(generics.ListAPIView):    
    serializer_class = EstudioPadronSerializer    
    queryset = DriEstudioPadron.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosPadronListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        estudios = self.get_queryset()
        print self.request.query_params
        try:
            tributo =self.request.query_params.get('tributo', None) 
            if tributo:
                    estudios = estudios.filter(tributo=tributo)
        except:
            pass
        try:
            id_unidad =self.request.query_params.get('id_unidad', None) 
            if id_unidad:
                    estudios = estudios.filter(id_unidad=id_unidad)
        except:
            pass
        try:
            anio_desde =self.request.query_params.get('anio_desde', None) 
            if anio_desde:
                    estudios = estudios.filter(anio__gte=anio_desde)
        except:
            pass
        try:
            anio_hasta =self.request.query_params.get('anio_hasta', None) 
            if anio_hasta:
                    estudios = estudios.filter(anio__lte=anio_hasta)
        except:
            pass
        cant=len(estudios)
        serializer = EstudioPadronSerializer(estudios, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class EstudiosPadronCreateView(BulkCreateAPIView):
    serializer_class = EstudioPadronSerializer    
    queryset = DriEstudioPadron.objects.all()
    permission_classes = (AllowAny,)
  

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosPadronCreateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def create(self, request, *args, **kwargs):
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)        
        if serializer.is_valid():
            vd = serializer.validated_data                        
            try:
                with transaction.atomic():
                    self.perform_create(serializer)       
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.validated_data)

            response_data["success"]=True
            response_data["message"]="%s EstudioPadron(es) Agregado(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_201_CREATED
            response_data["detalle"] = [v['id_negocio'] for v in vd]
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class EstudiosPadronUpdateView(BulkUpdateAPIView):
    serializer_class = EstudioPadronSerializer    
    queryset = DriEstudioPadron.objects.all()
    permission_classes = (AllowAny,)
  

    def dispatch(self, *args, **kwargs):
        response = super(EstudiosPadronUpdateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries
        return response


    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data                                    
            try:
                with transaction.atomic():
                    self.perform_bulk_update(serializer)           
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)          

            response_data["success"]=True
            response_data["message"]="%s EstudiosPadron(es) Actualizado(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_200_OK
            response_data["detalle"] = [v['id_negocio'] for v in vd]
            
            return Response(response_data, status=status.HTTP_200_OK)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)        

class EstudiosPadronDestroyView(generics.GenericAPIView):        
    permission_classes = (AllowAny,)
    serializer_class = EstudioPadronSerializer
    

    def dispatch(self, request, *args, **kwargs):
        response = super(EstudiosPadronDestroyView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def delete(self, request, *args, **kwargs):
        id_estudios_padron = []
        estudios_padron = None
        cant = 0
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=cant
        response_data["detalle"]=id_estudios_padron
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)      
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                id_estudios_padron = [v['id_negocio'] for v in vd]
                with transaction.atomic():                    
                    estudios_padron = DriEstudioPadron.objects.filter(id_negocio__in=id_estudios_padron)
                    cant = estudios_padron.count()                   
                    estudios_padron = estudios_padron.delete()
            except Exception as e:
                response_data["debug"]=str(e)
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data["detalle"] = id_estudios_padron            
            response_data["success"]=True
            response_data["message"]="%s Estudios Padron(es) Eliminado(s)" % cant
            response_data["cantidad"]=cant
            response_data["debug"]= str(id_estudios_padron)
            response_data["status"]=status.HTTP_201_CREATED
            return Response(response_data, status=status.HTTP_201_CREATED)
       
        response_data["message"]= str(serializer.errors)
        response_data["debug"]=str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)        

################################ DRI CuotasActividades GET/POST/PUT/DELETE ############################

class DRICuotaActListView(generics.ListAPIView):    
    serializer_class = DRICuotaActivCuotasSerializer    
    queryset = DriCuotaActividad.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(DRICuotaActListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        drica = self.get_queryset()
        print self.request.query_params
        try:
            id_padron =self.request.query_params.get('id_padron', None) 
            if id_padron:
                    drica = drica.filter(id_padron=id_padron)
        except:
            pass
        try:
            id_actividad =self.request.query_params.get('id_actividad', None) 
            if id_unidad:
                    drica = drica.filter(id_actividad=id_actividad)
        except:
            pass
        try:
            id_cuota =self.request.query_params.get('id_cuota', None) 
            if id_cuota:
                    drica = drica.filter(id_cuota=id_cuota)
        except:
            pass      
        try:
            id_boleta =self.request.query_params.get('id_boleta', None) 
            if id_boleta:
                    drica = drica.filter(id_boleta=id_boleta)
        except:
            pass     
        cant=len(drica)
        serializer = DRICuotaActivCuotasSerializer(drica, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class DRICuotaActCreateView(BulkCreateAPIView):
    queryset = DriCuotaActividad.objects.all()
    serializer_class = DRICuotaActivCuotasSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(DRICuotaActCreateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def create(self, request, *args, **kwargs):
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)        
        if serializer.is_valid():
            vd = serializer.validated_data                        
            try:
                with transaction.atomic():
                    self.perform_create(serializer)       
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            headers = self.get_success_headers(serializer.validated_data)

            response_data["success"]=True
            response_data["message"]="%s Cuota(s) Agregada(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_201_CREATED
            response_data["detalle"] = [v['id_cuota'] for v in vd]
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class DRICuotaActUpdateView(BulkUpdateAPIView):
    queryset = DriCuotaActividad.objects.all()
    serializer_class = DRICuotaActivCuotasSerializer
  

    def dispatch(self, *args, **kwargs):
        response = super(DRICuotaActUpdateView, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries
        return response


    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=0
        response_data["detalle"]=[]
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data                                    
            try:
                with transaction.atomic():
                    self.perform_bulk_update(serializer)           
            except Exception as e:
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)          

            response_data["success"]=True
            response_data["message"]="%s CuotaActiv Actualizada(s)" % len(vd)
            response_data["cantidad"]=len(vd)
            response_data["status"]=status.HTTP_200_OK
            response_data["detalle"] = [v['id_cuota'] for v in vd]
            
            return Response(response_data, status=status.HTTP_200_OK)
        response_data["message"]= str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)        

class DRICuotaActDestroyView(generics.GenericAPIView):        
    permission_classes = (AllowAny,)
    serializer_class = DRICuotaActivCuotasSerializer
    

    def dispatch(self, request, *args, **kwargs):
        response = super(DRICuotaActDestroyView, self).dispatch(request, *args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        return response

    def delete(self, request, *args, **kwargs):
        id_cuotas = []
        cuotas = None
        cant = 0
        response_data["success"]=False
        response_data["message"]=None
        response_data["debug"]=None
        response_data["cantidad"]=cant
        response_data["detalle"]=id_cuotas
        is_many = True if isinstance(request.data, list) else False
        serializer = self.get_serializer(data=request.data, many=is_many)      
        if serializer.is_valid():
            vd = serializer.validated_data
            try:
                id_cuotas = [v['id_cuota_actividad'] for v in vd]
                with transaction.atomic():                    
                    cuotas = DriCuotaActividad.objects.filter(id_cuota_actividad__in=id_cuotas)
                    cant = cuotas.count()                   
                    cuotas = cuotas.delete()
            except Exception as e:
                response_data["debug"]=str(e)
                response_data["message"]=str(e)
                response_data["status"]=status.HTTP_400_BAD_REQUEST                
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            response_data["detalle"] = id_cuotas            
            response_data["success"]=True
            response_data["message"]="%s CuotaActiv Eliminada(s)" % cant
            response_data["cantidad"]=cant
            response_data["debug"]= str(cuotas)
            response_data["status"]=status.HTTP_201_CREATED
            
            
            return Response(response_data, status=status.HTTP_201_CREATED)
       
        response_data["message"]= str(serializer.errors)
        response_data["debug"]=str(serializer.errors)
        response_data["status"]=status.HTTP_400_BAD_REQUEST                
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


################################ WEB Liquidaciones GET ############################

class WebLiqListView(generics.ListAPIView):    
    serializer_class = WebLiqSerializer    
    queryset = WEB_Liquidacion.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(WebLiqListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        liq = self.get_queryset()
        print self.request.query_params
        try:
            id_liquidacion =self.request.query_params.get('id_liquidacion', None) 
            if id_liquidacion:
                    liq = liq.filter(id_liquidacion=id_liquidacion)
        except:
            pass
        try:
            id_unidad =self.request.query_params.get('id_unidad', None) 
            if id_unidad:
                    liq = liq.filter(id_unidad=id_unidad)
        except:
            pass      
        cant=len(liq)
        serializer = WebLiqSerializer(liq, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class WebLiqCtasListView(generics.ListAPIView):    
    serializer_class = WebLiqCtasSerializer    
    queryset = WEB_Liquidacion_ctas.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(WebLiqCtasListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        liq = self.get_queryset()
        print self.request.query_params
        try:
            id_liquidacion =self.request.query_params.get('id_liquidacion', None) 
            if id_liquidacion:
                    liq = liq.filter(id_liquidacion__pk=id_liquidacion)
        except:
            pass
        try:
            id_cuota =self.request.query_params.get('id_cuota', None) 
            if id_cuota:
                    liq = liq.filter(id_cuota__pk=id_cuota)
        except:
            pass      
        cant=len(liq)
        serializer = WebLiqCtasSerializer(liq, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

################################ Suscriptores GET ############################

class SuscriptoresListView(generics.ListAPIView):    
    serializer_class = SuscriptoresSerializer    
    queryset = Suscriptores.objects.all()
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(SuscriptoresListView, self).dispatch(*args, **kwargs)
        print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        liq = self.get_queryset()
        print self.request.query_params
        try:
            tributo =self.request.query_params.get('tributo', None) 
            if tributo:
                    liq = liq.filter(tributo=tributo)
        except:
            pass
        try:
            id_padron =self.request.query_params.get('id_padron', None) 
            if id_padron:
                    liq = liq.filter(id_padron=id_padron)
        except:
            pass      
        cant=len(liq)
        serializer = SuscriptoresSerializer(liq, many=True)
        return Response({'data':serializer.data,'cantidad':cant})










################################ CUOTAS/BOLETAS VIEWSETS ############################

class APICuotasViewSet(viewsets.ModelViewSet):        
    serializer_class = CuotasSerializer
    allowed_methods = ("GET", "PUT")
    queryset = Cuotas.objects.all()
    # permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        response = super(APICuotasViewSet, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries) 
        # print connection.queries       
        return response
    

    def list(self,*args, **kwargs):
        cuotas = self.get_queryset()
        
        try:
            tributo =self.request.query_params.get('tributo', None) 
            if tributo:
                    cuotas = cuotas.filter(tributo=tributo)
        except:
            pass
        try:
            id_unidad =self.request.query_params.get('id_unidad', None) 
            if id_unidad:
                    cuotas = cuotas.filter(id_unidad=id_unidad)
        except:
            pass
        try:
            anio_desde =self.request.query_params.get('anio_desde', None) 
            if anio_desde:
                    cuotas = cuotas.filter(anio__gte=anio_desde)
        except:
            pass
        try:
            anio_hasta =self.request.query_params.get('anio_hasta', None) 
            if anio_hasta:
                    cuotas = cuotas.filter(anio__lte=anio_hasta)
        except:
            pass
        cant=len(cuotas)
        serializer = CuotasSerializer(cuotas, many=True)
        return Response({'data':serializer.data,'cantidad':cant})

class APIBoletasViewSet(viewsets.ModelViewSet):
    serializer_class = BoletasSerializer
    queryset = DriBoleta.objects.all().prefetch_related('boleta_actividades__id_boleta',)       
    permission_classes = (AllowAny,)


    def dispatch(self, *args, **kwargs):
        response = super(APIBoletasViewSet, self).dispatch(*args, **kwargs)
        # print "Cantidad de Queries:%s" % len(connection.queries)
        # for query in connection.queries:
            # print query['sql']
        return response

    def list(self, request ):
        boletas = self.get_queryset()
        cant=len(boletas)
        serializer = BoletasSerializer(boletas, many=True)
        return Response({'data':serializer.data,'cantidad':cant})
        # return Response({'data':boletas,'cantidad':cant})

       





def generarCodBar(idc,total1,total2,vencimiento,vencimiento2):
    """Devuelve el Codigo de Barras de 48/60 dígitos"""    
    try:
        c = Cuotas.objects.get(id_cuota=idc) 
    except:
        return None
    try:
        sitio = Configuracion.objects.all().first()
        diasExtra = sitio.diasextravencim
    except Configuracion.DoesNotExist:
        return None
   
    if diasExtra == None:
        diasExtra=0

    hoy = date.today()
    if (not vencimiento)and(not vencimiento2):
        vencimiento=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[0]
        vencimiento2=correr_vencimiento(c.vencimiento,c.segundo_vencimiento,c.tributo)[1]

        if (hoy >= c.vencimiento):
            vencimiento = hoy + relativedelta(days=diasExtra)   
            vencimiento2 = vencimiento
        else:
            vencimiento = c.vencimiento
            
        if c.segundo_vencimiento==None:
               vencimiento2 = vencimiento + relativedelta(months=1)
        elif (hoy <= c.segundo_vencimiento):
               vencimiento2 = c.segundo_vencimiento   
    try:
        longCB =sitio.longitudCodigoBarra
        if not sitio.longitudCodigoBarra:
            longCB = 48    
    except:
        longCB = 48
    
    try:               
        if (longCB==60)or((longCB<=60)and(float(total2)>=100000)):                    
            cod = generarCB60(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)            
        else:
            cod = generarCB48(sitio.id,c.tributo.id_tributo,vencimiento,total1,vencimiento2,total2,c.id_cuota,c.anio,c.cuota)
    except:
        return None    
    return cod

def generarCB48(codMuni,tributo,vencimiento,importe,vencimiento2,importe2,idCuotaLiq,anio,cuota):
    """Genera el código de Barras de 48 dígitos""" 
    #000 001 150120 869520231645821042000000010000000012020015
    cod = ""
    cod += str(codMuni).strip().rjust(3, "0")#CODIGO DEL MUNICIPIO
    cod += str(tributo).strip().rjust(3, "0") #TRIBUTO/LIQUIDACION WEB    
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(importe).strip().replace(".","").rjust(7, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(importe2).strip().replace(".","").rjust(7, "0") #Importe2 Actualizado
    cod += str(idCuotaLiq).strip().rjust(9, "0") #Id Liquidacion
    cod += str(anio).strip().rjust(4, "0") #Anio
    cod += str(cuota).strip().rjust(2, "0") #Cuota    
    cod += str(digVerificador(cod.strip()))    
    return cod

def generarCB60(codMuni,tributo,vencimiento,importe,vencimiento2,importe2,idCuotaLiq,anio,cuota):  
    """Genera el código de Barras de 60 dígitos""" 
    cod = "99999"
    cod += str(codMuni).strip().rjust(3, "0")#CODIGO DEL MUNICIPIO
    cod += str(tributo).strip().rjust(3, "0") #TRIBUTO/LIQUIDACION WEB
    cod += str(vencimiento.strftime("%d%m%y")).rjust(6, "0") #Vencimiento
    cod += str(importe).strip().replace(".","").rjust(10, "0") #Importe Actualizado
    cod += str(vencimiento2.strftime("%d%m%y")).rjust(6, "0") #Vencimiento2
    cod += str(importe2).strip().replace(".","").rjust(10, "0") #Importe2 Actualizado
    cod += str(idCuotaLiq).strip().rjust(10, "0") #Id Cuota
    cod += str(anio).strip().rjust(4, "0") #Anio   
    cod += str(cuota).strip().rjust(2, "0") #Cuota        
    cod += str(digVerificador(cod.strip()))    
    return cod

