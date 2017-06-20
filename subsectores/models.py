# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from lugar.models import Pais
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.

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
    nombre = models.CharField(max_length=250)
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
        return '%s - %s' % (self.nombre, self.pais.nombre)

    class Meta:
        verbose_name = 'Dato General (proyecto)'
        verbose_name_plural = 'Datos Generales (proyectos)'


@python_2_unicode_compatible
class ObjetivosResultados(models.Model):
    proyecto = models.ForeignKey(DatosGenerales)
    objetivo_corto = models.CharField(max_length=25, help_text='25 caracteres maximo')
    objetivo_completo = models.TextField()

    def __str__(self):
        return self.objetivo_corto

    class Meta:
        verbose_name = 'Objectivo de resultado'
        verbose_name_plural = 'Objectivo de resultados'


@python_2_unicode_compatible
class Indicadores(models.Model):
    objetivo = models.ForeignKey(ObjetivosResultados)
    descripcion_corto = models.CharField(max_length=25, help_text='25 caracteres maximo')
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
    #indicador = models.ForeignKey(Indicadores)
    indicador = ChainedForeignKey(
        Indicadores,
        chained_field="proyecto",
        chained_model_field="objetivo",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    nombre = models.CharField('Nombre de la actividad', max_length=250, help_text='Nombre completo de la actividad')
    categoria = models.ForeignKey(CategoriaGastos, verbose_name='Categoria de gatos')
    codigo_financiero = models.CharField(max_length=50)
    tipo_actividad = models.IntegerField(choices=CHOICES_TIPO_ACTIVIDAD,
                    help_text='Contribuye al dato del indicador',
                    verbose_name='Esta actividad contribuye')
    total_metas = models.FloatField(default=0, editable=False, null=True, blank=True)
    total_presupuesto = models.FloatField(default=0, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        total_meta = 0
        total_presupuesto = 0
        for item in self.registromeses_set.all():
            total_meta = total_meta + item.meta
            total_presupuesto = total_presupuesto + item.presupuesto

        self.total_metas = total_meta
        self.total_presupuesto =  total_presupuesto
        super(RegistroPlanAnual, self).save(*args, **kwargs)

    def __str__(self):
        return self.proyecto.nombre

    class Meta:
        verbose_name = 'Registro plan de actividad anual'
        verbose_name_plural = 'Registros planes de actividades anuales'


CHOICES_MESES = ((1,'1er trimestre'),(2,'2do trimestre'),
                 (3,'3er trimestre'),(4,'4to trimestre'),
                )

@python_2_unicode_compatible
class RegistroMeses(models.Model):
    registro_anual = models.ForeignKey(RegistroPlanAnual)
    mes = models.IntegerField(choices=CHOICES_MESES, verbose_name='Trimestres')
    anios = models.IntegerField('años')
    meta = models.FloatField()
    presupuesto = models.FloatField()

    def __str__(self):
        return self.registro_anual.nombre

    class Meta:
        verbose_name = 'Registro de mes'
        verbose_name_plural = 'Registro de meses'
