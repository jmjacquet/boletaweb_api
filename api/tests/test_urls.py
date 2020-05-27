# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from api.models import Cuotas
from django.urls import reverse
from rest_framework import status
import json

class TestCuotasAPI(APITestCase):
	
	def setUp(self):
		self.cuotas = [{
			"id_cuota": 1,
			"cuota": 9,
			"anio": 2020,
			"estado_nombre": "NORMAL",
			"id_responsable": 1051,
			"tributo": 6,
			"id_unidad": 331,
			"saldo": "1800.00",
			"vencimiento": "15/10/2020",
			"id_padron": "1961",
			"padron": "000/000",
			"fechapago": None,
			"estado": 0,
			"segundo_vencimiento": "15/11/2020",
			"nombre": "",
			"nombre_boleta": "",
			"nrodocu": "",
			"sexo": "",
			"calle": "",
			"numero": None,
			"piso": "",
			"depto": "",
			"localidad": "",
			"codseg": None,
			"fecha_audit": "08/05/2020 20:33:00"
		}]


	def test_create_cuotas(self):		
		response = self.client.post(reverse("api_cuotas_create"), data=self.cuotas,format='json')		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Cuotas.objects.count(), 1)

	def test_list_cuotas(self):
		response = self.client.post(reverse("api_cuotas_create"), data=self.cuotas,format='json')		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		response = self.client.get(reverse("api_cuotas_list"),format='json')		
		self.assertEqual(response.status_code, 200)
		rta = json.loads(response.content).get('data')		
		self.assertEqual(len(rta),1)
		
