# -*- coding: utf-8 -*-
from datetime import datetime, timedelta,date
from dateutil.relativedelta import *
import decimal
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import constants as message_constants
import datetime

ESTADOS = (
    (0, 'NORMAL'),
    (1, 'CONVENIO'),
    (100, 'JUDICIAL'),
    (1000, 'PAGO PENDIENTE'),
)

TIPOUSR = (
    (0, 'Contribuyente'),
    (1, 'Estudio Contable'),
    (2, 'Municipio'),
)

response_data = {
                "success": True,
                "message": "",
                "cantidad": None,
                "status": None,
                "detalle":[],
                "debug":None,
                "queries":None,
                "id_cuotas":[]
            }

acciones = {'I'}

def digVerificador(num):
    lista = list(num)
    pares= lista[1::2]
    impares= lista[0::2]
    
    totPares = 0
    totImpares = 0

    for i in pares:
        totPares=totPares+int(i*3)

    for i in impares:
        totImpares=totImpares+int(i)
 
    final = totImpares+totPares

    while (final > 9):
        cad=str(final)
        tot=0
        for i in cad:
            tot=tot+int(i)
        final=tot

    return final


def inicioMes():# pragma: no cover
    hoy=date.today()
    hoy = date(hoy.year,hoy.month,1)
    return hoy

def hoy():# pragma: no cover
    return date.today()    
    
def correr_vencimiento(vencimiento,vencimiento2,tributo):
    ''' Sirve para correr el vencimiento n dias si está entre la fdesde y fhasta definido en el tributo'''
    try:
        correr_venc_fdesde = tributo.correr_venc_fdesde
        if not vencimiento2:
            vencimiento2 = vencimiento
            
        if not correr_venc_fdesde:
            return [vencimiento,vencimiento2]
        
        correr_venc_fhasta = tributo.correr_venc_fhasta
        correr_venc_dias = tributo.correr_venc_dias
        if not correr_venc_fhasta:
            correr_venc_fhasta=date(3000,1,1)
        
        if not correr_venc_dias:
            correr_venc_dias = 0

        if (vencimiento >= correr_venc_fdesde)and(vencimiento <= correr_venc_fhasta):
            vencimiento = vencimiento + relativedelta(days=correr_venc_dias)               
            vencimiento2 = vencimiento2 + relativedelta(days=correr_venc_dias)
                 
        return [vencimiento,vencimiento2]
    except:
        return [vencimiento,vencimiento2]




MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}
