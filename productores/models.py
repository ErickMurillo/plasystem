# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField

# Create your models here.
SI_NO_CHOICES = ((1,'Si'),(2,'No'))
SEXO_CHOICES = ((1,'Mujer'),(2,'Hombre'))

class Productor(models.Model):
    nombre = models.CharField(max_length = 200,verbose_name = '1. Nombre y apellido')
    fecha_naciemiento = models.DateField(verbose_name = '2. Fecha de nacimiento')
    sexo = models.IntegerField(choices = SEXO_CHOICES,verbose_name = '3. Sexo')
    organizacion = models.ForeignKey(Organizacion,verbose_name = '4. Organización a la que pertenece')
    anios_vinculacion =  models.FloatField(verbose_name = '6. Años de vinculación')
    pais = models.ForeignKey(Pais)
    departamento = ChainedForeignKey(Departamento,chained_field="pais",chained_model_field="pais")
    municipio = ChainedForeignKey(Municipio,chained_field="departamento",chained_model_field="departamento")
    latitud = models.FloatField()
    longitud = models.FloatField()

FAMILIA_CHOICES = ((1,'Hombres > 31 años'),(2,'Mujeres > 31 años'),(3,'Ancianos > 64 años'),
                    (4,'Ancianas > 64 años'),(5,'Mujer joven de 19 a 30 años'),(6,'Hombre joven de 19 a 30 años'),
                    (7,'Mujer adolescente 13 a 18 años'),(8,'Hombre adolescente 13 a 18 años'),(9,'Niñas 5 a 12 años'),
                    (10,'Niños 5 a 12 años'),(11,'Niñas 0 a 4 años'),(12,'Niños 0 a 4 años'))

class MiembrosFamilia(models.Model):
    productor = models.ForeignKey(Productor)
    miembros = models.IntegerField(choices = FAMILIA_CHOICES)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = '7. Cantidad de miembros de la familia'
        verbose_name_plural = '7. Cantidad de miembros de la familia'

class DuenoPropiedad(models.Model):
    productor = models.ForeignKey(Productor)
    respuesta = models.IntegerField(choices = SI_NO_CHOICES)

    class Meta:
        verbose_name = '8. ¿Es dueño de la propiedad/finca?'
        verbose_name_plural = '8. ¿Es dueño de la propiedad/finca?'

DUENO_SI_CHOICES = ((1,'A nombre del hombre'),(2,'A nombre de la mujer'),
                    (3,'A nombre de los hijos'),(4,'Mancomunado'))

class DuenoSi(models.Model):
    productor = models.ForeignKey(Productor)
    si = models.IntegerField(choices = DUENO_SI_CHOICES)

    class Meta:
        verbose_name = 'En el caso SI, indique a nombre de quien está'
        verbose_name_plural = 'En el caso SI, indique a nombre de quien está'

DUENO_NO_CHOICES = ((1,'Arrendada'),(2,'Tierra Ind/comunal'),
                    (3,'Promesa de venta'),(4,'Sin escritura'),
                    (5,'Prestada'),(6,'Colectivo/Cooperativa'))

class DuenoNo(models.Model):
    productor = models.ForeignKey(Productor)
    no = models.IntegerField(choices = DUENO_NO_CHOICES)

    class Meta:
        verbose_name = 'En el caso que diga NO, especifique la situación'
        verbose_name_plural = 'En el caso que diga NO, especifique la situación'

#encuesta
class Encuestador(models.Model):
    nombre = models.CharField(max_length = 250)

GRUPO_CHOICES = ((1,'Grupo de intervención'),(2,'Grupo de control'))
class Encuesta(models.Model):
    grupo = models.IntegerField(choices = GRUPO_CHOICES)
    encuestador = models.ForeignKey(Encuestador)
    productor = models.ForeignKey(Productor)
    fecha = models.DateField()

class AreaFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    area = models.FloatField(verbose_name = 'Área',help_text='Mz')

    class Meta:
        verbose_name = '9. Área total de propiedad/finca'
        verbose_name_plural = '9. Área total de propiedad/finca'

DISTRIBUCION_CHOICES = ((1,'Bosque'),(2,'Potrero'),(3,'Cultivo anual'),(4,'Cultivo asociado'),
                        (5,'Plantación forestal'),(6,'Sistema agroforestal'),(7,'Sistema silvopastoril'))

class DistribucionFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    seleccion = models.IntegerField(choices = DISTRIBUCION_CHOICES)
    cantidad = models.FloatField()

    class Meta:
        verbose_name = '9.1 Distribución de la tierra en la propiedad/finca en Mz'
        verbose_name_plural = '9.1 Distribución de la tierra en la propiedad/finca en Mz'

class Certificacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    certificacion = models.IntegerField(choices = SI_NO_CHOICES)

    class Meta:
        verbose_name = '10. ¿La propiedad/ finca tiene certificación?'
        verbose_name_plural = '10. ¿La propiedad/ finca tiene certificación?'

CERTIFICACION_CHOICES = ((1,'Colectiva'),(2,'Individual'))

class TipoCertificacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo = models.IntegerField(choices = CERTIFICACION_CHOICES)

    class Meta:
        verbose_name = '10.1_En el caso SI, indique si la certificación es'
        verbose_name_plural = '10.1_En el caso SI, indique si la certificación es'

class Certificado(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Certificado que posee el productor'
        verbose_name_plural = 'Certificados que posee el productor'

class EmpresaCertifica(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Empresa que certifica al productor'
        verbose_name_plural = 'Empresas que certifican al productor'

class CertificadoEmpresa(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    certificado = models.ManyToManyField(Certificado)
    empresa = models.ManyToManyField(EmpresaCertifica)

    class Meta:
        verbose_name = '10.2_En el caso SI, indique el tipo de certificación y nombre de la empresa'
        verbose_name_plural = '10.2_En el caso SI, indique el tipo de certificación y nombre de la empresa'

class EliminacionFocos(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Eliminación de focos de contaminación dentro y fuera del cultivo'
        verbose_name_plural = 'Eliminación de focos de contaminación dentro y fuera del cultivo'

class ProteccionFuentes(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Protección de fuentes y calidad de agua (pozos, ríos)'
        verbose_name_plural = 'Protección de fuentes y calidad de agua (pozos, ríos)'

HIGIENE_CHOICES = ((1,'Lavado de manos'),(2,'Dispone de letrina'),(3,'Obreros no poseen enfermedades infecciosas'))

SUSTANCIAS_CHOICES = ((1,'Bodega de plaguicidas e insumos'),(2,'Área de preparación y mezclado de plaguicidas'),
                    (3,'Equipo protector para las personas que manipulan plaguicidas'))

class BPA(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    elimincacion_focos = models.ManyToManyField(EliminacionFocos,verbose_name = '1. Eliminación de focos de contaminación dentro y fuera del cultivo',blank=True)
    proteccion_fuentes = models.ManyToManyField(ProteccionFuentes,verbose_name = '2. Protección de fuentes y calidad de agua (pozos, ríos)',blank=True)
    higiene_trabajadores = MultiSelectField(choices = HIGIENE_CHOICES,blank = True,verbose_name = '3. Higiene de los trabajadores')
    sustancias_quimicas = MultiSelectField(choices = SUSTANCIAS_CHOICES,blank = True,verbose_name = '4. Uso correcto de sustancias químicas en')
    registro_rastreabilidad = models.BooleanField(blank = True,verbose_name = 'Registro y Rastreabilidad')

    class Meta:
        verbose_name = '11. ¿Si tiene Buenas Prácticas Agrícolas (BPA), indique el tipo de prácticas que implementa'
        verbose_name_plural = '11. ¿Si tiene Buenas Prácticas Agrícolas (BPA), indique el tipo de prácticas que implementa'

UNIDAD_MEDIDA = ((1,'Lb'),(2,'Unidades'),(3,'Docena'),(2,'Quintal'))

class Cultivo(models.Model):
    nombre = models.CharField(max_length = 250)
    unidad_medida = models.IntegerField(choices = UNIDAD_MEDIDA)
    hortaliza = models.BooleanField(blank = True)

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'

COLECTIVO_CHOICES = ((1,'Individual'),(2,'Asocio'))

class Produccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivo)
    forma_colectivo = models.IntegerField(choices = COLECTIVO_CHOICES)
    area_sembrada = models.FloatField(verbose_name = 'Área sembrada (Mz)')
    area_cosechada = models.FloatField(verbose_name = 'Área cosechada (Mz)')
    cantidad_cosechada = models.FloatField(verbose_name = 'Cantidad cosechada')
    consumo = models.FloatField(verbose_name = 'Consumo de la familia')
    procesamiento = models.FloatField()
    venta = models.FloatField()
    costo_produccion = models.FloatField(verbose_name = 'Costo producción por Mz (Moneda local)')
    costo_inversion = models.FloatField(verbose_name = 'Costo inversión por Mz (Moneda local)')

    class Meta:
        verbose_name = '12. Indique producción y destino de cada uno de los cultivos establecidos en la propiedad/finca'
        verbose_name_plural = '12. Indique producción y destino de cada uno de los cultivos establecidos en la propiedad/finca'
