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

class Instituciones(models.Model):
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
    institucion = models.ForeignKey(Instituciones)
    areas = models.ManyToManyField(Areas)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.institucion.nombre


class OrganizacionPertenece(models.Model):
    organizaciones = models.ManyToManyField(Instituciones)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.organizaciones.nombre

    class Meta:
        verbose_name_plural = 'Organizaciones a la que pertenece'

CHOICE_MIEMBROS = (
    (1, 'Número de miembros registrados oficialmente'),
    (2, 'Número de miembros en proceso de afiliación'),
    )

class MiembrosOficiales(models.Model):
    opcion = models.IntegerField(choices=CHOICE_MIEMBROS)
    total_hombre = models.IntegerField()
    total_mujer = models.IntegerField()
    activos_hombre = models.IntegerField()
    activos_mujer = models.IntegerField()
    jovenes_hombre = models.IntegerField()
    jovenes_mujer = models.IntegerField()
    inactivos_hombre = models.IntegerField()
    inactivos_mujer = models.IntegerField()


    organizacion = models.ForeignKey(Organizacion)

    

class NumeroCooperativa(models.Model):
    numero_cooperativa = models.IntegerField()

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return '%s' % str(self.numero_cooperativa)

CHOICE_PROVEEDORES = (
    (1, 'Número de miembros registrados oficialmente'),
    
    )

class ProductoresProveedores(models.Model):
    opcion = models.IntegerField(choices=CHOICE_PROVEEDORES)
    total_hombre = models.IntegerField()
    total_mujer = models.IntegerField()
    activos_hombre = models.IntegerField()
    activos_mujer = models.IntegerField()
    jovenes_hombre = models.IntegerField()
    jovenes_mujer = models.IntegerField()

    organizacion = models.ForeignKey(Organizacion)

    

CHOICE_EMPLEADOS = (
    (1, 'Tiempo completo'),
    (2, 'Tiempo parcial'),
    (3, 'Temporales')
    )

class EmpleadosOrganizacion(models.Model):
    opcion = models.IntegerField(choices=CHOICE_EMPLEADOS)
    total_hombre = models.IntegerField()
    total_mujer = models.IntegerField()
    adultos_hombre = models.IntegerField()
    adultos_mujer = models.IntegerField()
    jovenes_hombre = models.IntegerField()
    jovenes_mujer = models.IntegerField()

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.get_opcion_display()

CHOICE_TRANSITABLE = (
    (1, 'Transitable todo el tiempo'),
    (2, 'Transitable solo en verano'),
    )

class Infraestructura(models.Model):
    vias_finca = models.CharField(max_length=250)
    transitable_finca = models.IntegerField(choices=CHOICE_TRANSITABLE)
    vias_oficina = models.CharField(max_length=250)
    transitable_oficina = models.IntegerField(choices=CHOICE_TRANSITABLE)
    distancia = models.CharField(max_length=150)
    acceso_internet = models.CharField(max_length=150, choices=CHOICE_SI_NO)
    transporte_publico = models.CharField(max_length=150, choices=CHOICE_SI_NO)
    red_movil = models.CharField(max_length=150, choices=CHOICE_SI_NO)
    electricidad = models.CharField(max_length=150, choices=CHOICE_SI_NO)
    agua_potable = models.CharField(max_length=150, choices=CHOICE_SI_NO)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.vias_finca

CHOICE_SECTOR = (
    (1, 'Agricultura'),
    (2, 'Ganadería'),
    (3, 'Forestal'),
    (4, 'Acuicultura'),
    )

class SectoresProductos(models.Model):
    sector = models.IntegerField(choices=CHOICE_SECTOR)
    producto = models.CharField(max_length=250)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.get_sector_display()


class Actividades(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

class Actividad(models.Model):
    actividad = models.ForeignKey(Actividades)
    socios = models.IntegerField(choices=CHOICE_SI_NO)
    no_socios = models.IntegerField(choices=CHOICE_SI_NO)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.get_actividad_display()

class Servicios(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

class Servicio(models.Model):
    servicio = models.ForeignKey(Servicios)
    socios = models.IntegerField(choices=CHOICE_SI_NO)
    no_socios = models.IntegerField(choices=CHOICE_SI_NO)

    organizacion = models.ForeignKey(Organizacion)

    def __unicode__(self):
        return self.get_actividad_display()

