# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *
from multiselectfield import MultiSelectField
from productores.models import Cultivo

# Create your models here.
class Digitador(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Digitador'
        verbose_name_plural = 'Digitadores'

class ResultadosEvaluacion(models.Model):
    digitador = models.ForeignKey(Digitador)
    fecha = models.DateField()
    organizacion = models.ForeignKey(Organizacion)

    year = models.IntegerField(editable=False)

    def save(self):
        self.year = self.fecha.year
        super(ResultadosEvaluacion, self).save()

    def __unicode__(self):
        return self.organizacion.nombre

    class Meta:
        verbose_name = 'V. Resultados de evaluación SCOPE Pro'
        verbose_name_plural = 'V. Resultados de evaluación SCOPE Pro'

CHOICE_GESTION = (
        (1, 'Total Gestion interna'),
        (2, 'Gobernabilidad'),
        (3, 'Organización interna'),
        (4, 'Planificación de negocios')
    )

class GestionInterna(models.Model):
    opciones = models.IntegerField(choices=CHOICE_GESTION)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '1.Gestión Interna'
        verbose_name_plural = '1.Gestión Interna'


CHOICE_OPERACIONES = (
        (1, 'Total operaciones'),
        (2, 'Logistica, almacenamiento y tecnología'),
        (3, 'Producción'),
        (4, 'Procesamiento')
    )

class Operaciones(models.Model):
    opciones = models.IntegerField(choices=CHOICE_OPERACIONES)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '2. Operaciones'
        verbose_name_plural = '2. Operaciones'

CHOICE_SOSTENIBILIDAD = (
        (1, 'Total sostenibilidad'),
        (2, 'Aspectos Sociales'),
        (3, 'Aspectos ambientales')
    )

class Sostenibilidad(models.Model):
    opciones = models.IntegerField(choices=CHOICE_SOSTENIBILIDAD)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '3. Sostenibilidad'
        verbose_name_plural = '3. Sostenibilidad'


CHOICE_GESTION_FINANCIERA = (
        (1, 'Total gestión financiera'),
        (2, 'Gestión financiera'),
        (3, 'Planificación financiera'),
        (4, 'Registro de información y monitoreo')
    )

class GestionFinanciera(models.Model):
    opciones = models.IntegerField(choices=CHOICE_GESTION_FINANCIERA)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '4. Gestión financiera'
        verbose_name_plural = '4. Gestión financiera'


CHOICE_DESEMPENO_FINANCIERO = (
        (1, 'Total Desempeño financiero'),
        (2, 'Balance General'),
        (3, 'Estado de resultado'),
        (4, 'Pérdidas y ganancias')
    )

class DesempenoFinanciero(models.Model):
    opciones = models.IntegerField(choices=CHOICE_DESEMPENO_FINANCIERO)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '5. Desempeño financiero'
        verbose_name_plural = '5. Desempeño financiero'


CHOICE_SUMINISTROS = (
        (1, 'Total suministros'),
        (2, 'Adquisición'),
        (3, 'Logística de entrada'),
        (4, 'Contratación de miembros/agr. Ext.'),
        (5, 'Supervisión y cap.de productores'),
        (6, 'Servicios financieros a miembros'),
    )

class Suministros(models.Model):
    opciones = models.IntegerField(choices=CHOICE_SUMINISTROS)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '6. Suministro'
        verbose_name_plural = '6. Suministro'


CHOICE_MERCADOS = (
        (1, 'Total mercados'),
        (2, 'Riesgo relacionado con el mercado'),
        (3, 'Logística de salida'),
        (4, 'Estrategias de mercadeo'),
    )

class Mercados(models.Model):
    opciones = models.IntegerField(choices=CHOICE_MERCADOS)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '7. Mercados'
        verbose_name_plural = '7. Mercados'


CHOICE_RIESGOS_EXTERNOS = (
        (1, 'Total riesgo externo'),
        (2, 'Conocimiento de riesgos nat. y climat.'),
        (3, 'Mitigación de riesgos nat. y climat.'),
        (4, 'Conocimiento de riesgos biol. y amb.'),
        (5, 'Mitigación de riesgos biológicos y amb.')
    )

class RiesgoExternos(models.Model):
    opciones = models.IntegerField(choices=CHOICE_RIESGOS_EXTERNOS)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '8.Riesgo externo'
        verbose_name_plural = '8.Riesgo externo'


CHOICE_FACILITADORES = (
        (1, 'Total facilitadores'),
        (2, 'Desarrolladores de capacidades y ONG'),
        (3, 'Proveedores de servicios'),
        (4, 'Organizaciones del sector'),
        (5, 'Comunidad'),
        (6, 'Gobierno y regulaciones')
    )

class Facilitadores(models.Model):
    opciones = models.IntegerField(choices=CHOICE_FACILITADORES)
    valor = models.FloatField()
    mejoras = models.TextField('Principales Mejoras Realizadas (Describa)')
    limitante = models.TextField('Principales Áreas a Mejorar/Limitantes (Describa)')

    resultado = models.ForeignKey(ResultadosEvaluacion)

    class Meta:
        verbose_name = '9. Facilitadores'
        verbose_name_plural = '9. Facilitadores'


# -------------------Resultado implementado del programa --------------------------

CHOICE_PARA_QUIEN = ((1, 'Adultos mayores de 35 años'),(2, 'Jóvenes menores de 35 años'))

class ResultadosImplementacion(models.Model):
    digitador = models.ForeignKey(Digitador)
    fecha = models.DateField()
    organizacion = models.ForeignKey(Organizacion)
    para_quien = models.IntegerField(choices=CHOICE_PARA_QUIEN)

    year = models.IntegerField(editable=False)

    def save(self):
        self.year = self.fecha.year
        super(ResultadosImplementacion, self).save()

    def __unicode__(self):
        return self.organizacion.nombre

    class Meta:
        verbose_name = 'VI. Resultados implementación del programa'
        verbose_name_plural = 'VI. Resultados implementación del programa'



CHOICES_34_1 = (
        (1, 'a) Producen y comercializan de forma colectiva'),
        (2, 'b) Producen productos sanos'),
        (3, 'c) Tienen contratos de largo plazo'),
    )

class ProducenComercializan(models.Model):
    opcion = models.IntegerField(choices=CHOICES_34_1)
    cantidad_hombres = models.IntegerField()
    cantidad_mujeres = models.IntegerField()
    cultivo = models.ForeignKey(Cultivo)
    area_hombre_sembrada = models.FloatField()
    area_mujer_sembrada = models.FloatField()
    area_hombre_cosechada = models.FloatField()
    area_mujer_cosechada = models.FloatField()
    unidad_medida = models.CharField(max_length=50)
    cantidad = models.FloatField()
    cantidad_certificada = models.FloatField()
    precio_promedio = models.FloatField()

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = '34.1 Productores que producen y comercializan de forma colectiva'

CHOICE_CONTRATO = (
        (1, 'c.1) Contrato escrito'),
        (2, 'c.2) Contrato verbal'),
    )

class AcuerdoComercial(models.Model):
    tipo_contrato = models.IntegerField(choices=CHOICE_CONTRATO, null=True, blank=True)
    periodo = models.CharField('c.3.Periodo del contrato', max_length=150, null=True, blank=True)

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = 'Acuerdo comerciales'


CHOICE_TIPO_MERCADO = (
        (1, 'Tradicional'),
        (2, 'Feria'),
        (3, 'Local'),
        (4, 'Empresa comercializadora'),
        (5, 'Empresa procesadora'),
        (6, 'Empresas exportadoras'),
        (7, 'Supermercado'),
        (8, 'Cadena de restaurantes'),
        (9, 'Intermediarios'),
    )

class IncrementoAbastecimiento(models.Model):
    comprador = models.CharField(max_length=250)
    cantidad_hombres = models.IntegerField()
    cantidad_mujeres = models.IntegerField()
    tipo_mercado = models.IntegerField(choices = CHOICE_TIPO_MERCADO)

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = '34.2 Cantidad de productores que incremento de volumen'


CHOICE_AUMENTADO_INGRESOS = (
        (1, 'Café'),
        (2, 'Cacao'),
        (3, 'Hostalizas'),

    )


class AumentadoIngresos(models.Model):
    opcion = models.IntegerField(choices=CHOICE_AUMENTADO_INGRESOS)
    cantidad_hombres = models.IntegerField()
    cantidad_mujeres = models.IntegerField()
    area_hombre_sembrada = models.FloatField()
    area_mujer_sembrada = models.FloatField()
    area_hombre_cosechada = models.FloatField()
    area_mujer_cosechada = models.FloatField()
    unidad_medida = models.CharField(max_length=50)
    cantidad = models.FloatField()
    cantidad_certificada = models.FloatField()
    precio_promedio = models.FloatField()
    precio_promedio_certificada = models.FloatField(default=0)

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = '34.3 Cantidad de productores aumentado ingresos'


class AumentadoProductividad(models.Model):
    cantidad_hombres = models.IntegerField()
    cantidad_mujeres = models.IntegerField()
    area_hombre_sembrada = models.FloatField()
    area_mujer_sembrada = models.FloatField()
    area_hombre_cosechada = models.FloatField()
    area_mujer_cosechada = models.FloatField()
    unidad_medida = models.CharField(max_length=50)
    cantidad = models.FloatField()
    cantidad_certificada = models.FloatField()
    precio_promedio = models.FloatField()
    precio_promedio_certificada = models.FloatField(default=0)

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = '35 productividad (kg/ha) de cacao fermentado seco'