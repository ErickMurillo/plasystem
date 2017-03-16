# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField

# Create your models here.
SI_NO_CHOICES = (('Si','Si'),('No','No'))
SEXO_CHOICES = (('Mujer','Mujer'),('Hombre','Hombre'))

class Productor(models.Model):
    nombre = models.CharField(max_length = 200,verbose_name = '1. Nombre y apellido')
    fecha_naciemiento = models.DateField(verbose_name = '2. Fecha de nacimiento')
    sexo = models.CharField(max_length = 5,choices = SEXO_CHOICES,verbose_name = '3. Sexo')
    organizacion = models.ForeignKey(Organizacion,verbose_name = '4. Organización a la que pertenece')
    anios_vinculacion =  models.FloatField(verbose_name = '6. Años de vinculación')
    pais = models.ForeignKey(Pais)
    departamento = ChainedForeignKey(Departamento,chained_field="pais",chained_model_field="pais")
    municipio = ChainedForeignKey(Municipio,chained_field="departamento",chained_model_field="departamento")
    latitud = models.FloatField()
    longitud = models.FloatField()

FAMILIA_CHOICES = (('Hombres > 31 años','Hombres > 31 años'),('Mujeres > 31 años','Mujeres > 31 años'),('Ancianos > 64 años','Ancianos > 64 años'),
                    ('Ancianas > 64 años','Ancianas > 64 años'),('Mujer joven de 19 a 30 años','Mujer joven de 19 a 30 años'),('Hombre joven de 19 a 30 años','Hombre joven de 19 a 30 años'),
                    ('Mujer adolescente 13 a 18 años','Mujer adolescente 13 a 18 años'),('Hombre adolescente 13 a 18 años','Hombre adolescente 13 a 18 años'),('Niñas 5 a 12 años','Niñas 5 a 12 años'),
                    ('Niños 5 a 12 años','Niños 5 a 12 años'),('Niñas 0 a 4 años','Niñas 0 a 4 años'),('Niños 0 a 4 años','Niños 0 a 4 años'))

class MiembrosFamilia(models.Model):
    productor = models.ForeignKey(Productor)
    miembros = models.CharField(max_length = 50,choices = FAMILIA_CHOICES)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = '7. Cantidad de miembros de la familia'
        verbose_name_plural = '7. Cantidad de miembros de la familia'

class DuenoPropiedad(models.Model):
    productor = models.ForeignKey(Productor)
    respuesta = models.CharField(max_length = 5,choices = SI_NO_CHOICES)

    class Meta:
        verbose_name = '8. ¿Es dueño de la propiedad/finca?'
        verbose_name_plural = '8. ¿Es dueño de la propiedad/finca?'

DUENO_SI_CHOICES = (('A nombre del hombre','A nombre del hombre'),('A nombre de la mujer','A nombre de la mujer'),
                    ('A nombre de los hijos','A nombre de los hijos'),('Mancomunado','Mancomunado'))

class DuenoSi(models.Model):
    productor = models.ForeignKey(Productor)
    si = models.CharField(max_length = 50,choices = DUENO_SI_CHOICES)

    class Meta:
        verbose_name = 'En el caso SI, indique a nombre de quien está'
        verbose_name_plural = 'En el caso SI, indique a nombre de quien está'

DUENO_NO_CHOICES = (('Arrendada','Arrendada'),('Tierra Ind/comunal','Tierra Ind/comunal'),
                    ('Promesa de venta','Promesa de venta'),('Sin escritura','Sin escritura'),
                    ('Prestada','Prestada'),('Colectivo/Cooperativa','Colectivo/Cooperativa'))

class DuenoNo(models.Model):
    productor = models.ForeignKey(Productor)
    no = models.CharField(max_length = 50,choices = DUENO_NO_CHOICES)

    class Meta:
        verbose_name = 'En el caso que diga NO, especifique la situación'
        verbose_name_plural = 'En el caso que diga NO, especifique la situación'

#encuesta
class Encuestador(models.Model):
    nombre = models.CharField(max_length = 250)

GRUPO_CHOICES = (('Grupo de intervención','Grupo de intervención'),('Grupo de control','Grupo de control'))
class Encuesta(models.Model):
    grupo = models.CharField(max_length = 50,choices = GRUPO_CHOICES)
    encuestador = models.ForeignKey(Encuestador)
    productor = models.ForeignKey(Productor)
    fecha = models.DateField()

class AreaFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    area = models.FloatField(verbose_name = 'Área',help_text='Mz')

    class Meta:
        verbose_name = '9. Área total de propiedad/finca'
        verbose_name_plural = '9. Área total de propiedad/finca'

DISTRIBUCION_CHOICES = (('Bosque','Bosque'),('Potrero','Potrero'),('Cultivo anual','Cultivo anual'),('Cultivo asociado','Cultivo asociado'),
                        ('Plantación forestal','Plantación forestal'),('Sistema agroforestal','Sistema agroforestal'),('Sistema silvopastoril','Sistema silvopastoril'))

class DistribucionFinca(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    seleccion = models.CharField(max_length = 50,choices = DISTRIBUCION_CHOICES)
    cantidad = models.FloatField()

    class Meta:
        verbose_name = 'Distribución de la tierra'
        verbose_name_plural = '9.1 Distribución de la tierra en la propiedad/finca en Mz'

class Certificacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    certificacion = models.CharField(max_length = 5,choices = SI_NO_CHOICES)

    class Meta:
        verbose_name = '10. ¿La propiedad/ finca tiene certificación?'
        verbose_name_plural = '10. ¿La propiedad/ finca tiene certificación?'

CERTIFICACION_CHOICES = (('Colectiva','Colectiva'),('Individual','Individual'))

class TipoCertificacion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo = models.CharField(max_length = 50,choices = CERTIFICACION_CHOICES)

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

HIGIENE_CHOICES = (('Lavado de manos','Lavado de manos'),('Dispone de letrina','Dispone de letrina'),('Obreros no poseen enfermedades infecciosas','Obreros no poseen enfermedades infecciosas'))

SUSTANCIAS_CHOICES = (('Bodega de plaguicidas e insumos','Bodega de plaguicidas e insumos'),('Área de preparación y mezclado de plaguicidas','Área de preparación y mezclado de plaguicidas'),
                    ('Equipo protector para las personas que manipulan plaguicidas','Equipo protector para las personas que manipulan plaguicidas'))

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

UNIDAD_MEDIDA = (('Lb','Lb'),('Unidades','Unidades'),('Docena','Docena'),('Quintal','Quintal'))

class Cultivo(models.Model):
    nombre = models.CharField(max_length = 250)
    unidad_medida = models.CharField(max_length = 50,choices = UNIDAD_MEDIDA)
    hortaliza = models.BooleanField(blank = True)

    def __str__(self):
        return u'%s - %s' % (self.nombre,self.unidad_medida)

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'

COLECTIVO_CHOICES = (('Individual','Individual'),('Asocio','Asocio'))

class Produccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivo)
    forma_colectivo = models.CharField(max_length = 50,choices = COLECTIVO_CHOICES)
    area_sembrada = models.FloatField(verbose_name = 'Área sembrada (Mz)')
    area_cosechada = models.FloatField(verbose_name = 'Área cosechada (Mz)')
    cantidad_cosechada = models.FloatField(verbose_name = 'Cantidad cosechada')
    consumo = models.FloatField(verbose_name = 'Consumo de la familia')
    procesamiento = models.FloatField()
    venta = models.FloatField()
    costo_produccion = models.FloatField(verbose_name = 'Costo producción por Mz (Moneda local)')
    costo_inversion = models.FloatField(verbose_name = 'Costo inversión por Mz (Moneda local)')

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = '12. Indique producción y destino de cada uno de los cultivos establecidos en la propiedad/finca'

class DestinoProduccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivo)

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = '13. Por tipo de cultivo, según la cantidad destinada la venta, indique cantidad vendida por tipo de mercado y precio(moneda local)'


MERCADO_CHOICES = (('Mercado tradicional','Mercado tradicional'),('Cooperativa','Cooperativa'),('Ferias','Ferias'),('Empresas procesadoras','Empresas procesadoras'),
                    ('Empresas comercializadoras','Empresas comercializadoras'),('Empresas exportadoras','Empresas exportadoras'),('Supermercados','Supermercados'),
                    ('Cadena de restaurantes','Cadena de restaurantes'),('Intermediarios','Intermediarios'))

class Mercado(models.Model):
    destino_produccion = models.ForeignKey(DestinoProduccion)
    mercado = models.CharField(max_length = 50,choices = MERCADO_CHOICES)
    cantidad = models.FloatField()
    precio = models.FloatField()

class IngresosOtrosCultivos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivo)
    ingreso_anual = models.FloatField(verbose_name = 'Ingreso anual (moneda local)')

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = '14. ¿Indique los ingresos totales por otros cultivos en la propiedad/finca?'

class IngresosFamilia(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.IntegerField(choices = SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '15. ¿La familia percibe otros ingresos diferentes a la actividad agrícola?'

FUENTE_INGRESOS_CHOICES = (('Asalariado','Asalariado'),('Jornalero','Jornalero'),('Alquiler','Alquiler'),
                            ('Negocio propio','Negocio propio'),('Remesas','Remesas'),('Otros','Otros'))

class FuenteIngresos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    fuente_ingreso = models.CharField(max_length = 50,choices = FUENTE_INGRESOS_CHOICES)
    cantidad_mensual = models.IntegerField(verbose_name = 'Cantidad total mensual (Moneda local)')
    cantidad_veces = models.IntegerField(verbose_name = 'Cantidad de veces en el año que recibe esta cantidad')
    hombres = models.IntegerField(verbose_name = 'Cantidad de miembros hombres de la familia involucrados')
    mujeres = models.IntegerField(verbose_name = 'Cantidad de miembros mujeres de la familia involucrados')

    class Meta:
        verbose_name = 'Fuente de ingreso'
        verbose_name_plural = '15.1. Si la respuesta es SI puede indicar la fuente'

GANADERIA_CHOICES = (('Ganadería menor','Ganadería menor'),('Ganadería mayor','Ganadería mayor'),
                    ('Procesamiento de productos agrícolas','Procesamiento de productos agrícolas'))

class IngresosActividadesGanaderia(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    seleccion = models.CharField(max_length = 50,choices = GANADERIA_CHOICES)
    cantidad_mensual = models.IntegerField(verbose_name = 'Cantidad total mensual (Moneda local)')
    cantidad_veces = models.IntegerField(verbose_name = 'Cantidad de veces en el año que recibe esta cantidad')

    class Meta:
        verbose_name = 'Fuente de ingreso'
        verbose_name_plural = '16. Otros ingresos por actividades de ganadería (mayor y menor) y procesamiento de productos agropecuarios'

class TipoSistemaRiego(models.Model):
    nombre = models.CharField(max_length = 150)

    class Meta:
        verbose_name = 'Tipo de sistema de riego'
        verbose_name_plural = 'Tipos de sistemas de riego'

ESTADO_CHOICES = (('Bueno','Bueno'),('Regular','Regular'),('Malo','Malo'))

class CondicionesRiegos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    sistema_riego = models.CharField(max_length = 5,choices = SI_NO_CHOICES,verbose_name = '17. ¿Dispone de sistema de riego?')
    tipo_sistema_riego = models.ForeignKey(TipoSistemaRiego,verbose_name = '17.1 ¿Tipo de sistema de riego posee?',null = True, blank = True)
    estado_sistema_riego = models.CharField(max_length = 50,choices = ESTADO_CHOICES,verbose_name = '17.2 ¿Cual es el estado del sistema de riego?',null = True, blank = True)
    area_sistema_riego = models.FloatField(verbose_name = '17.3 ¿Cantidad de área en mz  bajo sistema de riego?',null = True, blank = True)
    cosecha_agua = models.CharField(max_length = 5,choices = SI_NO_CHOICES,verbose_name = '18 ¿Tiene cosecha de agua?')

    class Meta:
        verbose_name_plural = 'Condiciones de riegos de la propiedad/finca'

EROSION_CHOICES = ((1,'Ninguna erosión y ninguna compactación del suelo'),
                    (2,'Erosión del suelo en pequeña escala o compacto con medidas adoptadas'),
                    (3,'Erosión del suelo a gran escala pero con medidas adoptadas'),
                    (4,'Erosión del suelo a gran escala pero sin medidas'),
                    )

SANILIZACION_CHOICES = ((1,'No hay historia de muy alto nivel de salinidad del suelo'),
                        (2,'Algunos casos de la salinidad del suelo, con las medidas adoptadas'),
                        (3,'Casos frecuentes de la salinidad del suelo, pero con medidas adoptadas'),
                        (4,'Casos frecuentes de la salinidad del suelo sin medidas adoptadas'),
                        )

CONTAMINACION_CHOICES = ((1,'Niveles aceptables de contaminación (metales pesados, biológicas) en el suelo sobre la base de datos de prueba de suelo'),
                         (2,'Pocos casos de contaminación adoptando medidas'),
                         (3,'Casos frecuentes de contaminación, sino adoptan medidas'),
                         (4,'Casos frecuentes de contaminación sin medidas')
                        )

MATERIA_CHOICES = ((1,'Sin quema, acumulación de materia orgánica del suelo'),
                    (2,'Pocos casos de quema, aumento de la materia orgánica'),
                    (3,'Frecuentes casos de quema pero han adoptados medidas'),
                    (4,'Casos frecuentes de quema sin medidas adoptadas')
                  )

class ConservacionSuelo(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    erosion = models.IntegerField(choices = EROSION_CHOICES,verbose_name = '19.1 Erosión y/o compactación')
    sanilizacion = models.IntegerField(choices = SANILIZACION_CHOICES,verbose_name = '19.2 Salinización')
    contaminacion_suelo = models.IntegerField(choices = CONTAMINACION_CHOICES,verbose_name = '19.3 Contaminación del suelo')
    materia_organica = models.IntegerField(choices = MATERIA_CHOICES,verbose_name = '19.4 Materia orgánica y el ciclo de nutrientes')

    class Meta:
        verbose_name_plural = '19. Conservación de suelo'

GESTION_CHOICES = ((1,'El uso del agua para producir está optimizado'),
                    (2,'El uso del agua es más eficiente con las medidas adoptadas'),
                    (3,'El uso de agua no es eficiente, pero han adoptados medidas'),
                    (4,'Uso ineficiente del agua sin medidas adoptadas')
                    )

RETENCION_CHOICES = ((1,'No hay casos de agua de escorrentía, tiene retención de agua'),
                    (2,'Algunos casos de la escorrentía y con las medidas adoptadas'),
                    (3,'Casos frecuentes de escorrentía sino se toman medidas'),
                    (4,'Casos frecuentes de escorrentía sin medidas')
                    )

EFICIENCIA_CHOICES = ((1,'El uso del agua en comparación con la salida está optimizado'),
                        (2,'El uso del agua es más eficiente con las medidas adoptadas'),
                        (3,'El uso de agua no es eficiente, si no toman medidas'),
                        (4,'Uso ineficiente del agua sin medidas')
                        )

CONTAMINACION_AGUA_CHOICES = ((1,'Mínima contaminación de cuerpos de agua naturales (probado con regularidad en la comunidad)'),
                            (2,'Pocos casos de contaminación y las medidas adoptadas para mejorar las condiciones'),
                            (3,'Casos frecuentes de contaminación, pero realizan pruebas del agua y toman medidas'),
                            (4,'Contaminación frecuente, sin agua y sin medidas para mejorar las condiciones')
                            )

class UsoEficienteAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    gestion_riesgo = models.IntegerField(choices = GESTION_CHOICES,verbose_name = '20.1 Gestión del riego')
    retencion_agua = models.IntegerField(choices = RETENCION_CHOICES,verbose_name = '20.2 Retención de agua y la escorrentía')
    eficiencia_agua = models.IntegerField(choices = EFICIENCIA_CHOICES,verbose_name = '20.3 Eficiencia del Agua (aplicable para el procesamiento)')
    contaminacion_agua = models.IntegerField(choices = CONTAMINACION_AGUA_CHOICES,verbose_name = '20.4 Contaminación del agua')

    class Meta:
        verbose_name_plural = '20. El uso eficiente del agua y calidad del agua'

PRUEBAS_CHOICES = ((1,'El análisis del suelo es realizado recientemente en terreno/Granja/FO nivel que sea homogéneo'),
                    (2,'Se realiza el análisis del suelo, pero los datos son mayores de 5 años y no refleja las condiciones no homogéneos'),
                    (3,'Los datos de análisis de suelo no está disponible pero se han tomado medidas para obtener datos de suelos'),
                    (4,'No se dispone de datos de pruebas del suelo y ninguna de las medidas adoptadas para obtener datos')
                    )

MANEJO_NUTRIENTES = ((1,'Manejo de nutrientes es altamente eficiente'),
                    (2,'Manejo de nutrientes es casi eficiente y toman medidas'),
                    (3,'Manejo de nutrientes es ineficiente, sino se toman medidas'),
                    (4,'Manejo de nutrientes es ineficaz sin las medidas adoptadas')
                    )

FERTILIZANTE_ORGANICO = ((1,'Se ha optimizado el uso de fertilizantes orgánicos'),
                        (2,'El uso de fertilizantes orgánicos es casi óptima con las medidas adoptadas'),
                        (3,'El uso de fertilizantes orgánicos está lejos de ser óptima con las medidas adoptadas'),
                        (4,'El uso de fertilizantes orgánicos está lejos de optimizar sin las medidas adoptadas')
                        )

BALANCE_CHOICES = ((1,'Balance de N y P en la granja se mantiene'),
                    (2,'N y P fuera de equilibrio con las medidas adoptadas'),
                    (3,'N y P gravemente desequilibrado, pero tomar contramedidas')
                    )

RESIDUOS_CHOICES = ((1,'Agricultura orgánica sin dejar residuos, tales como contenedores de nocivos en el medio ambiente'),
                    (2,'Aplicación de un sistema para recoger, devolver o la eliminación segura de los envases de agroquímicos'),
                    (3,'Sin gestión de residuos agroquímicos, pero las medidas adoptadas'),
                    (4,'Sin gestión de residuos de agroquímicos y sin medidas')
                    )

class GestionRecursosNaturales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    pruebas_suelo = models.IntegerField(choices = PRUEBAS_CHOICES,verbose_name = '21.1 Pruebas del suelo')
    manejo_nutrientes = models.IntegerField(choices = MANEJO_NUTRIENTES,verbose_name = '21.2 Manejo de nutrientes')
    fertilizante_organico = models.IntegerField(choices = FERTILIZANTE_ORGANICO,verbose_name = '21.3 Fertilizante orgánico')
    balance = models.IntegerField(choices = BALANCE_CHOICES,verbose_name = '21.4 Balance de nitrógeno y fósforo')
    gestion_residuos = models.IntegerField(choices = RESIDUOS_CHOICES,verbose_name = '21.5 Gestión de los residuos de la producción para procesar')
    gestion_envases = models.IntegerField(choices = ENVASES_CHOICES,verbose_name = '21.6 Gestión de envases vacíos de agroquímicos y productos agroquímicos sobrantes')
