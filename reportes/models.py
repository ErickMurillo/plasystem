# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lugar.models import *

# Create your models here.
class Reporte(models.Model):
	titulo = models.CharField(max_length=200)
	fecha_elaborado = models.DateField()
	donante = models.CharField(max_length=200)
	subsector = models.CharField(max_length=200)
	pais = models.ForeignKey(Pais)
	archivo = models.FileField(upload_to='reportes/')