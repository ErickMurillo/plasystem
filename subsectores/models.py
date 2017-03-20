# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from lugar.models import Pais

# Create your models here.

@python_2_unicode_compatible
class Componentes(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

CHOICES_MONEDA = ((1,'USD$'),)

@python_2_unicode_compatible
class DatosGenerales(models.Model):
    componente = models.ForeignKey(Componentes)
    anio = models.IntegerField('Año')
    pais = models.ForeignKey(Pais)
    responsable = models.CharField('Nombre del responsable', max_length=250)
    moneda = models.IntegerField(choices=CHOICES_MONEDA)
    grupo = models.CharField('Grupo Meta', max_length=250)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Dato General'
        verbose_name_plural = 'Datos Generales'


@python_2_unicode_compatible
class ObjetivosResultados(models.Model):
    objetivo_corto = models.TextField()
    objetivo_completo = models.TextField()

    def __str__(self):
        return self.objetivo_corto

    class Meta:
        verbose_name = 'Objectivo de resultado'
        verbose_name_plural = 'Objectivo de resultados'



@python_2_unicode_compatible
class Indicadores(models.Model):
    descripcion_corto = models.TextField()
    descripcion_completo = models.TextField()
    objetivo = models.ForeignKey(ObjetivosResultados)

    def __str__(self):
        return self.descripcion_corto

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'


@python_2_unicode_compatible
class Aspectos(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Aspecto'
        verbose_name_plural = 'Aspectos'


CHOICES_ASPECTO = ((1,'Rojo(<)'),(2,'Verde(>)'),)

@python_2_unicode_compatible
class UmbrelaDesempeno(models.Model):
    aspecto = models.ForeignKey(Aspectos)
    nivel = models.IntegerField(choices=CHOICES_ASPECTO)

    def __str__(self):
        return self.aspecto.nombre

    class Meta:
        verbose_name = 'Umbrela de desempeño'
        verbose_name_plural = 'Umbrelas de desempeños'

#--------- registro de planes anuales --------

@python_2_unicode_compatible
class TipoItem(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo item'
        verbose_name_plural = 'Tipos items'

@python_2_unicode_compatible
class Actividades(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'


@python_2_unicode_compatible
class CategoriaGastos(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoria de gasto'
        verbose_name_plural = 'Categorias de gatos'


@python_2_unicode_compatible
class RegistroPlanAnual(models.Model):
    item = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoItem)
    indicador = models.ForeignKey(Indicadores)
    actividad = models.ForeignKey(Actividades)
    indicador2 = models.CharField(max_length=250)
    categoria = models.ForeignKey(CategoriaGastos)

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = 'Registro plan anual'
        verbose_name_plural = 'Registros planes anuales'


CHOICES_MESES = ((1,'Enero'),(2,'Febrero'),
                 (3,'Marzo'),(4,'Abril'),
                 (5,'Mayo'),(6,'Junio'),
                 (7,'Julio'),(8,'Agosto'),
                 (9,'Septiembre'),(10,'Octubre'),
                 (11,'Noviembre'),(12,'Diciembre'),)

@python_2_unicode_compatible
class RegistroMeses(models.Model):
    registro_anual = models.ForeignKey(RegistroPlanAnual)
    mes = models.IntegerField(choices=CHOICES_MESES)
    meta = models.FloatField()
    presupuesto = models.FloatField()
    

    def __str__(self):
        return self.registro_anual.item

    class Meta:
        verbose_name = 'Registro de mes'
        verbose_name_plural = 'Registro de meses'

