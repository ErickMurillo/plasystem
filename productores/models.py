# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TipoOrganizacion(models.Model):
    nombre = models.CharField(max_length = 200)

class Organizacion(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo = models.ForeignKey(TipoOrganizacion)

SI_NO_CHOICES = ((1,'Si'),(0,'No'))

class Productor(models.Model):
    nombre = models.CharField(max_length = 200,verbose_name = 'Nombre y apellido')
    fecha_naciemiento = models.DateField()
    organizacion = models.ForeignKey(Organizacion,verbose_name = 'Organización a la que pertenece')
    anios_vinculacion =  models.FloatField(verbose_name = 'Años de vinculación')
    dueno_propiedad = models.IntegerField(choices = SI_NO_CHOICES)
    latitud = models.FloatField()
    longitud = models.FloatField()

DUENO_SI_CHOICES = ((1,'A nombre del hombre'),(2,'A nombre de la mujer'),
                    (3,'A nombre de los hijos'),(4,'Mancomunado'))

class DuenoSi(models.Model):
    productor = models.ForeignKey(Productor)
    si = models.IntegerField(choices = DUENO_SI_CHOICES)

DUENO_NO_CHOICES = ((1,'Arrendada'),(2,'Tierra Ind/comunal'),
                    (3,'Promesa de venta'),(4,'Sin escritura'),
                    (5,'Prestada'),(6,'Colectivo/Cooperativa'))

class DuenoNo(models.Model):
    productor = models.ForeignKey(Productor)
    no = models.IntegerField(choices = DUENO_NO_CHOICES)
