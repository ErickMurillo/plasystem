# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *
from multiselectfield import MultiSelectField

# Create your models here.
class Digitador(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

class ResultadosEvaluacion(models.Model):
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
        verbose_name = 'V. Resultados de evaluación SCOPE Pro'
        verbose_name_plural = 'V. Resultados de evaluación SCOPE Pro'

CHOICE_GESTION = (
        (1, 'Gobernabilidad'),
        (2, 'Organización interna'),
        (3, 'Planificación de negocios')
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
        (1, 'Logistica, almacenamiento y tecnología'),
        (2, 'Producción'),
        (3, 'Procesamiento')
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
        (1, 'Aspectos Sociales'),
        (2, 'Aspectos ambientales')
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
        (1, 'Gestión financiera'),
        (2, 'Planificación financiera'),
        (3, 'Registro de información y monitoreo')
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
        (1, 'Balance General'),
        (2, 'Estado de resultado'),
        (3, 'Pérdidas y ganancias')
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
        (1, 'Adquisición'),
        (2, 'Logística de entrada'),
        (3, 'Contratación de miembros/agr. Ext.'),
        (4, 'Supervisión y cap.de productores'),
        (5, 'Servicios financieros a miembros'),
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
        (1, 'Riesgo relacionado con el mercado'),
        (2, 'Logística de salida'),
        (3, 'Estrategias de mercadeo'),
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
        (1, 'Conocimiento de riesgos nat. y climat.'),
        (2, 'Mitigación de riesgos nat. y climat.'),
        (3, 'Conocimiento de riesgos biol. y amb.'),
        (4, 'Mitigación de riesgos biológicos y amb.')
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
        (1, 'Desarrolladores de capacidades y ONG'),
        (2, 'Proveedores de servicios'),
        (3, 'Organizaciones del sector'),
        (4, 'Comunidad'),
        (5, 'Gobierno y regulaciones')
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
    pais = models.ForeignKey('lugar.pais')
    organizacion = models.ForeignKey(Organizacion)
    para_quien = models.IntegerField(choices=CHOICE_PARA_QUIEN)

    year = models.IntegerField(editable=False)

    def save(self):
        self.year = self.fecha.year
        super(Encuesta, self).save()

    def __unicode__(self):
        return self.organizacion.nombre

    class Meta:
        verbose_name = 'VI. Resultados implementación del programa'
        verbose_name_plural = 'VI. Resultados implementación del programa'



CHOICES_34_1 = (
        (1, 'a) Producen y comercializan de forma colectiva'),
        (2, 'b) Producen productos sanos'),
        (3, 'c) Tienen contratos de largo plazo'),
        (4, 'c.1) Contrato escrito'),
        (5, 'c.2) Contrato verbal'),
        (6, 'c.3.) Periodo del contrato')
    )

class ProducenComercializan(models.Model):
    opcion = models.IntegerField(choices=CHOICES_34_1)
    cantidad_hombres = models.IntegerField()
    cantidad_mujeres = models.IntegerField()
    cultivo = models.CharField(max_length=250)
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


CHOICE_TIPO_MERCADO = (
        ('uno', 'Tradicional'),
        ('dos', 'Feria'),
        ('tres', 'Local'),
        ('cuatro', 'Empresa comercializadora'),
        ('cinco', 'Empresa procesadora'),
        ('seis', 'Empresas exportadoras'),
        ('siete', 'Supermercado'),
        ('ocho', 'Cadena de restaurantes'),
        ('nueve', 'Intermediarios'),
    )

class IncrementoAbastecimiento(models.Model):
    comprador = models.CharField(max_length=250)
    tipo_mercado = MultiSelectField(choices = CHOICE_TIPO_MERCADO)

    resultado_implementacion = models.ForeignKey(ResultadosImplementacion)

    class Meta:
        verbose_name_plural = '34.2 Cantidad de productores que incremento de volumen'