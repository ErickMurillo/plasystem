# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from lugar.models import *

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
    direccion = models.CharField(max_length=300, null=True, blank=True)
    pais = models.ForeignKey(Pais)
    departamento = models.ForeignKey(Departamento)
    municipio = models.ForeignKey(Municipio)
    oficina_numero = models.CharField(max_length=12, null=True, blank=True)
    oficina_correo = models.EmailField(max_length=254, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    #redes sociales
    red_social1 = models.CharField(max_length=250, null=True, blank=True)
    red_social2 = models.CharField(max_length=250, null=True, blank=True)
    red_social3 = models.CharField(max_length=250, null=True, blank=True)
    red_social4 = models.CharField(max_length=250, null=True, blank=True)
    #persona 1 de contacto
    persona1_contacto = models.CharField(max_length=300, null=True, blank=True)
    persona1_cargo = models.CharField(max_length=250, null=True, blank=True)
    persona1_telefono = models.CharField(max_length=12, null=True, blank=True)
    persona1_correo = models.EmailField(max_length=254, null=True, blank=True)
    #persona 2 de contacto
    persona2_contacto = models.CharField(max_length=300, null=True, blank=True)
    persona2_cargo = models.CharField(max_length=250, null=True, blank=True)
    persona2_telefono = models.CharField(max_length=12, null=True, blank=True)
    persona2_correo = models.EmailField(max_length=254, null=True, blank=True)



    def __str__(self):
		return self.nombre

    class Meta:
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'
