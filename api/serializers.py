# -*- coding: utf-8 -*-
from rest_framework import serializers,fields
from api.models import Cuotas,Tributo,DriBoleta,DriBoleta_actividades,DriEstudio,DriEstudioPadron,DriCuotaActividad,WEB_Liquidacion,WEB_Liquidacion_ctas,Suscriptores
from api.utilidades import ESTADOS
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin



class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]
        

class CuotaSerializer(serializers.ModelSerializer): 
	id_cuota = serializers.IntegerField()
	cuota = serializers.IntegerField()
	anio = serializers.IntegerField()
	estado_nombre = serializers.CharField(source="get_estado",read_only=True)
	accion = serializers.CharField(read_only=True)
	class Meta: 
		model = Cuotas
		fields = '__all__'		
		update_lookup_field = 'id_cuota'

class CuotasSerializer(BulkSerializerMixin,serializers.ModelSerializer): 
	id_cuota = serializers.IntegerField()
	cuota = serializers.IntegerField()
	anio = serializers.IntegerField()
	# estado_nombre = serializers.CharField(source="get_estado",read_only=True)
	class Meta: 
		model = Cuotas
		fields = '__all__'
		list_serializer_class = BulkListSerializer
		update_lookup_field = 'id_cuota'


class EstudioPadronSerializer(BulkSerializerMixin,serializers.ModelSerializer): 		
	id_negocio = serializers.IntegerField()
	class Meta: 
		model = DriEstudioPadron		
		fields = '__all__'
		list_serializer_class = BulkListSerializer
		update_lookup_field = 'id_negocio'

class EstudiosSerializer(BulkSerializerMixin,serializers.ModelSerializer): 
	id_estudioc = serializers.IntegerField()
	class Meta: 
		model = DriEstudio
		fields = '__all__'
		list_serializer_class = BulkListSerializer
		update_lookup_field = 'id_estudioc'

class DRICuotaActivCuotasSerializer(BulkSerializerMixin,serializers.ModelSerializer): 		
	id_cuota_actividad = serializers.IntegerField()
	id_cuota = serializers.IntegerField()
	class Meta: 
		model = DriCuotaActividad
		fields = '__all__'
		list_serializer_class = BulkListSerializer
		update_lookup_field = 'id_cuota_actividad'		

class Boletas_ActividadesSerializer(serializers.ModelSerializer): 			
	class Meta: 
		model = DriBoleta_actividades		
		fields = '__all__'

class BoletasSerializer(serializers.ModelSerializer): 		
	boleta_actividad = Boletas_ActividadesSerializer(many=True,read_only=True)		
	recargo = serializers.DecimalField(max_digits=15, decimal_places=2)
	total = serializers.DecimalField(max_digits=15, decimal_places=2)
	class Meta: 
		model = DriBoleta
		# exclude = ['fecha_audit']
		fields = '__all__'



class WebLiqCtasSerializer(serializers.ModelSerializer): 			
	class Meta: 
		model = WEB_Liquidacion_ctas		
		fields = '__all__'

class WebLiqSerializer(serializers.ModelSerializer): 		
	webliq_cuotas = WebLiqCtasSerializer(many=True,read_only=True)		
	class Meta: 
		model = WEB_Liquidacion
		# exclude = ['fecha_audit']
		fields = '__all__'


class SuscriptoresSerializer(serializers.ModelSerializer): 			
	class Meta: 
		model = Suscriptores
		fields = '__all__'











class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
