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

CHOICE_PERSONERIA = (
        (1, 'Si'),
        (2, 'No'),
        (3, 'En proceso')
    )

CHOICE_SI_NO = (
        (1, 'Si'),
        (2, 'No'),
    )

@python_2_unicode_compatible
class Organizacion(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo = models.ForeignKey(TipoOrganizacion)
    direccion = models.CharField(max_length=300, null=True, blank=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, null=True, blank=True)
    oficina_numero = models.CharField(max_length=12, null=True, blank=True)
    oficina_correo = models.EmailField(max_length=254, null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    #redes sociales
    red_social1 = models.CharField('Red Social 1', max_length=250, null=True, blank=True)
    red_social2 = models.CharField('Red Social 2', max_length=250, null=True, blank=True)
    red_social3 = models.CharField('Red Social 3', max_length=250, null=True, blank=True)
    red_social4 = models.CharField('Red Social 4', max_length=250, null=True, blank=True)
    #persona 1 de contacto
    persona1_contacto = models.CharField('Nombre', max_length=300, null=True, blank=True)
    persona1_cargo = models.CharField('Cargo', max_length=250, null=True, blank=True)
    persona1_telefono = models.CharField('Telefono', max_length=12, null=True, blank=True)
    persona1_correo = models.EmailField('Correo', max_length=254, null=True, blank=True)
    #persona 2 de contacto
    persona2_contacto = models.CharField('Nombre', max_length=300, null=True, blank=True)
    persona2_cargo = models.CharField('Cargo', max_length=250, null=True, blank=True)
    persona2_telefono = models.CharField('Telefono', max_length=12, null=True, blank=True)
    persona2_correo = models.EmailField('Correo', max_length=254, null=True, blank=True)
    #situacion legal
    personeria = models.IntegerField('Cuenta con personería Jurídica', choices=CHOICE_PERSONERIA, null=True, blank=True)
    en_operaciones = models.IntegerField(choices=CHOICE_SI_NO, null=True, blank=True)
    incorporacion = models.CharField('Año de incorporación', max_length=250, null=True, blank=True)
    licencia = models.CharField('No. de licencia empresarial', max_length=250, null=True, blank=True)
    tributaria = models.CharField('No. de identificación tributaria', max_length=250, null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    mision = models.TextField(null=True, blank=True)
    apoyo = models.IntegerField(choices=CHOICE_SI_NO, null=True, blank=True)


    def __str__(self):
		return self.nombre

    class Meta:
        verbose_name = 'Organización'
        verbose_name_plural = 'Organizaciones'

class Intituciones(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Instituciones'

class Areas(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Areas de apoyo'

class ApoyoDonante(models.Model):
    institucion = models.ForeignKey(Intituciones)
    areas = models.ManyToManyField(Areas)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.institucion.nombre