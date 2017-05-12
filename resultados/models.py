# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *

# Create your models here.
class Digitador(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

class EncuestasResultados(models.Model):
    digitador = models.ForeignKey(Digitador)
    fecha = models.DateField()
    pais = models.ForeignKey('lugar.pais')
    organizacion = models.ForeignKey(Organizacion)

    year = models.IntegerField(editable=False)

    def save(self):
        self.year = self.fecha.year
        super(Encuesta, self).save()

    def __unicode__(self):
        return self.organizacion.nombre

    class Meta:
        verbose_name = 'Resultados de Evaluación'
        verbose_name_plural = 'Resultados de Evaluación'



