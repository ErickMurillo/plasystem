# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from lugar.models import Pais
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.

@python_2_unicode_compatible
class Componentes(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

@python_2_unicode_compatible
class GruposMetas(models.Model):
    nombre = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Grupo meta'
        verbose_name_plural = 'Grupos metas'


@python_2_unicode_compatible
class Monedas(models.Model):
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo moneda'
        verbose_name_plural = 'Tipos de monedas'

class TipoCambiosMonedaPais(models.Model):
    pais = models.ForeignKey(Pais)
    moneda = models.ForeignKey(Monedas)

    def __str__(self):
        return '%s' % (self.moneda.nombre)

    class Meta:
        verbose_name = 'Tipo de cambio moneda por pais'
        verbose_name_plural = 'Tipos de cambios monedas por pais'

class TasaCambioPaisAnual(models.Model):
    tipo_cambio = models.ForeignKey(TipoCambiosMonedaPais)
    anio = models.IntegerField()
    dolar = models.FloatField(default=0)
    euro = models.FloatField(default=0)

    def __str__(self):
        return 'dolar: %s - euro: %s' % (self.dolar,self.euro)

    class Meta:
        verbose_name = 'Tasa de cambio anual'
        verbose_name_plural = 'Tasas de cambios anuales'


@python_2_unicode_compatible
class DatosGenerales(models.Model):
    componente = models.ForeignKey(Componentes)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    pais = models.ForeignKey(Pais)
    responsable = models.CharField('Nombre del responsable', max_length=250)
    #moneda = models.ForeignKey(TipoCambiosMonedaPais)
    moneda = ChainedForeignKey(
        TipoCambiosMonedaPais, 
        chained_field="pais",
        chained_model_field="pais", 
        show_all=False, 
        auto_choose=True,
        sort=True
    )
    grupo = models.ManyToManyField(GruposMetas)

    def __str__(self):
        return self.componente.nombre

    class Meta:
        verbose_name = 'Dato General (proyecto)'
        verbose_name_plural = 'Datos Generales (proyectos)'


@python_2_unicode_compatible
class ObjetivosResultados(models.Model):
    proyecto = models.ForeignKey(DatosGenerales)
    objetivo_corto = models.CharField(max_length=25)
    objetivo_completo = models.TextField()

    def __str__(self):
        return self.objetivo_corto

    class Meta:
        verbose_name = 'Objectivo de resultado'
        verbose_name_plural = 'Objectivo de resultados'


@python_2_unicode_compatible
class Indicadores(models.Model):
    objetivo = models.ForeignKey(ObjetivosResultados)
    descripcion_corto = models.CharField(max_length=25)
    descripcion_completo = models.TextField()
    codigo = models.CharField(max_length=50)
    programatico_mayor = models.FloatField()
    programatico_menor = models.FloatField()
    ejecucion_mayor = models.FloatField()
    ejecucion_menor = models.FloatField()
    
    def __str__(self):
        return self.descripcion_corto

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'

#--------- registro de planes anuales --------

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


CHOICES_TIPO_ACTIVIDAD = ((1,'Contribuye'),(2,'No contribuye'),)

@python_2_unicode_compatible
class RegistroPlanAnual(models.Model):
    proyecto = models.ForeignKey(DatosGenerales)
    actividad = models.ForeignKey(Actividades)
    categoria = models.ForeignKey(CategoriaGastos)
    codigo_financiero = models.CharField(max_length=50)
    tipo_actividad = models.IntegerField(choices=CHOICES_TIPO_ACTIVIDAD)
    indicador = models.ForeignKey(Indicadores)
    metas_indicador = models.FloatField(editable=False, null=True, blank=True)
    

    def __str__(self):
        return self.proyecto.componente.nombre

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
    anios = models.IntegerField()
    meta = models.FloatField()
    presupuesto = models.FloatField()
    

    def __str__(self):
        return self.registro_anual.actividad.nombre

    class Meta:
        verbose_name = 'Registro de mes'
        verbose_name_plural = 'Registro de meses'

