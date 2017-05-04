# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class TipoOrganizacion(models.Model):
    nombre = models.CharField(max_length = 200)

    def __str__(self):
		return self.nombre

    class Meta:
        verbose_name = 'Tipo de Organización'
        verbose_name_plural = 'Tipos de Organizaciones'

@python_2_unicode_compatible
class Organizacion(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo = models.ForeignKey(TipoOrganizacion)

    def __str__(self):
		return self.nombre

    class Meta:
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'
