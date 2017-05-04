# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from organizaciones.models import *
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField
from datetime import date
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
SI_NO_CHOICES = (('Si','Si'),('No','No'))
SEXO_CHOICES = (('Mujer','Mujer'),('Hombre','Hombre'))
EDAD_CHOICES = ((1,'Menor 35'),(2,'Mayor 35'))

@python_2_unicode_compatible
class Productor(models.Model):
    nombre = models.CharField(max_length = 200,verbose_name = '1. Nombre y apellido')
    fecha_naciemiento = models.DateField(verbose_name = '2. Fecha de nacimiento')
    sexo = models.CharField(max_length = 6,choices = SEXO_CHOICES,verbose_name = '3. Sexo')
    organizacion = models.ForeignKey(Organizacion,verbose_name = '4. Organización a la que pertenece')
    anios_vinculacion =  models.FloatField(verbose_name = '6. Años de vinculación')
    pais = models.ForeignKey(Pais)
    departamento = ChainedForeignKey(Departamento,chained_field="pais",chained_model_field="pais")
    municipio = ChainedForeignKey(Municipio,chained_field="departamento",chained_model_field="departamento")
    latitud = models.FloatField(null = True, blank = True)
    longitud = models.FloatField(null = True, blank = True)
    edad = models.IntegerField(editable = False,choices = EDAD_CHOICES)

    class Meta:
        verbose_name = 'Productor'
        verbose_name_plural = 'Productores'

    def save(self, *args, **kwargs):
        #calcular edad a partir de fecha nacimiento
        today = date.today()
        edad = today.year - self.fecha_naciemiento.year - ((today.month, today.day) < (self.fecha_naciemiento.month, self.fecha_naciemiento.day))
        if edad < 35:
            self.edad = 1
        else:
            self.edad = 2
        super(Productor, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


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

    class Meta:
        verbose_name = 'Encuestador'
        verbose_name_plural = 'Encuestadores'

    def __str__(self):
		return self.nombre.encode('utf-8')

GRUPO_CHOICES = (('Grupo de intervención','Grupo de intervención'),('Grupo de control','Grupo de control'))

class Encuesta(models.Model):
    grupo = models.CharField(max_length = 50,choices = GRUPO_CHOICES)
    encuestador = models.ForeignKey(Encuestador)
    productor = models.ForeignKey(Productor)
    fecha = models.DateField()
    anio = models.IntegerField(editable = False)

    def save(self, *args, **kwargs):
        self.anio = self.fecha.year
        super(Encuesta, self).save(*args, **kwargs)

    def __str__(self):
        return self.productor.nombre.encode('utf-8')

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


@python_2_unicode_compatible
class Certificado(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Certificado que posee el productor'
        verbose_name_plural = 'Certificados que posee el productor'

    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class EmpresaCertifica(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Empresa que certifica al productor'
        verbose_name_plural = 'Empresas que certifican al productor'

    def __str__(self):
        return self.nombre

class CertificadoEmpresa(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    certificado = models.ManyToManyField(Certificado)
    empresa = models.ManyToManyField(EmpresaCertifica)

    class Meta:
        verbose_name = '10.2_En el caso SI, indique el tipo de certificación y nombre de la empresa'
        verbose_name_plural = '10.2_En el caso SI, indique el tipo de certificación y nombre de la empresa'

@python_2_unicode_compatible
class EliminacionFocos(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Eliminación de focos de contaminación dentro y fuera del cultivo'
        verbose_name_plural = 'Eliminación de focos de contaminación dentro y fuera del cultivo'

    def __str__(self):
        return self.nombre

@python_2_unicode_compatible
class ProteccionFuentes(models.Model):
    nombre = models.CharField(max_length = 250)

    class Meta:
        verbose_name = 'Protección de fuentes y calidad de agua (pozos, ríos)'
        verbose_name_plural = 'Protección de fuentes y calidad de agua (pozos, ríos)'

    def __str__(self):
        return self.nombre

class BPAPregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta =  models.CharField(max_length = 5,choices = SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '11. ¿Aplica Buenas Prácticas Agrícolas (BPA)?'

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

UNIDAD_MEDIDA = (('Libra','Libra'),('Unidad','Unidad'),('Docena','Docena'),('Quintal','Quintal'))

CULTIVO_CHOICES = ((1,'Café'),(2,'Cacao'),(3,'Hortaliza'))

@python_2_unicode_compatible
class Cultivo(models.Model):
    nombre = models.CharField(max_length = 250)
    unidad_medida = models.CharField(max_length = 50,choices = UNIDAD_MEDIDA)
    # hortaliza = models.BooleanField(blank = True)
    tipo = models.IntegerField(choices = CULTIVO_CHOICES)

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
    archivo_costo_produccion = models.FileField(verbose_name = 'Archivo costo producción', blank = True, null = True)
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

    ingreso = models.FloatField(editable=False, default=0)

    def save(self):
        self.ingreso = self.cantidad * self.precio
        super(Mercado, self).save()

class IngresosOtrosCultivos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivo)
    ingreso_anual = models.FloatField(verbose_name = 'Ingreso anual (moneda local)')

    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = '14. ¿Indique los ingresos totales por otros cultivos en la propiedad/finca?'

class IngresosFamilia(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    respuesta = models.CharField(max_length = 5,choices = SI_NO_CHOICES)

    class Meta:
        verbose_name_plural = '15. ¿La familia percibe otros ingresos diferentes a la actividad agrícola?'

FUENTE_INGRESOS_CHOICES = (('Asalariado','Asalariado'),('Jornalero','Jornalero'),('Alquiler','Alquiler'),
                            ('Negocio propio','Negocio propio'),('Remesas','Remesas'),('Otros','Otros'))

class FuenteIngresos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    fuente_ingreso = models.CharField(max_length = 50,choices = FUENTE_INGRESOS_CHOICES)
    cantidad_mensual = models.IntegerField(verbose_name = 'Cantidad total mensual (Moneda local)')
    cantidad_veces = models.IntegerField(verbose_name = 'Cantidad de veces en el año que recibe esta cantidad')
    hombres = models.IntegerField(verbose_name = 'Hombres (Cantidad de miembros de la familia involucrados)')
    mujeres = models.IntegerField(verbose_name = 'Mujeres (Cantidad de miembros de la familia involucrados)')

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

@python_2_unicode_compatible
class TipoSistemaRiego(models.Model):
    nombre = models.CharField(max_length = 150)

    class Meta:
        verbose_name = 'Tipo de sistema de riego'
        verbose_name_plural = 'Tipos de sistemas de riego'

    def __str__(self):
        return self.nombre

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

EROSION_CHOICES = ((3,'Ninguna erosión y ninguna compactación del suelo'),
                    (2,'Erosión del suelo en pequeña escala o compacto con medidas adoptadas'),
                    (1,'Erosión del suelo a gran escala pero con medidas adoptadas'),
                    (0,'Erosión del suelo a gran escala pero sin medidas'),
                    )

SANILIZACION_CHOICES = ((3,'No hay historia de muy alto nivel de salinidad del suelo'),
                        (2,'Algunos casos de la salinidad del suelo, con las medidas adoptadas'),
                        (1,'Casos frecuentes de la salinidad del suelo, pero con medidas adoptadas'),
                        (0,'Casos frecuentes de la salinidad del suelo sin medidas adoptadas'),
                        )

CONTAMINACION_CHOICES = ((3,'Niveles aceptables de contaminación (metales pesados, biológicas) en el suelo sobre la base de datos de prueba de suelo'),
                         (2,'Pocos casos de contaminación adoptando medidas'),
                         (1,'Casos frecuentes de contaminación, sino adoptan medidas'),
                         (0,'Casos frecuentes de contaminación sin medidas')
                        )

MATERIA_CHOICES = ((3,'Sin quema, acumulación de materia orgánica del suelo'),
                    (2,'Pocos casos de quema, aumento de la materia orgánica'),
                    (1,'Frecuentes casos de quema pero han adoptados medidas'),
                    (0,'Casos frecuentes de quema sin medidas adoptadas')
                  )

class ConservacionSuelo(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    erosion = models.IntegerField(choices = EROSION_CHOICES,verbose_name = '19.1 Erosión y/o compactación')
    sanilizacion = models.IntegerField(choices = SANILIZACION_CHOICES,verbose_name = '19.2 Salinización')
    contaminacion_suelo = models.IntegerField(choices = CONTAMINACION_CHOICES,verbose_name = '19.3 Contaminación del suelo')
    materia_organica = models.IntegerField(choices = MATERIA_CHOICES,verbose_name = '19.4 Materia orgánica y el ciclo de nutrientes')

    class Meta:
        verbose_name_plural = '19. Conservación de suelo'

GESTION_CHOICES = ((3,'El uso del agua para producir está optimizado'),
                    (2,'El uso del agua es más eficiente con las medidas adoptadas'),
                    (1,'El uso de agua no es eficiente, pero han adoptados medidas'),
                    (0,'Uso ineficiente del agua sin medidas adoptadas')
                    )

RETENCION_CHOICES = ((3,'No hay casos de agua de escorrentía, tiene retención de agua'),
                    (2,'Algunos casos de la escorrentía y con las medidas adoptadas'),
                    (1,'Casos frecuentes de escorrentía sino se toman medidas'),
                    (0,'Casos frecuentes de escorrentía sin medidas')
                    )

EFICIENCIA_CHOICES = ((3,'El uso del agua en comparación con la salida está optimizado'),
                        (2,'El uso del agua es más eficiente con las medidas adoptadas'),
                        (1,'El uso de agua no es eficiente, si no toman medidas'),
                        (0,'Uso ineficiente del agua sin medidas')
                        )

CONTAMINACION_AGUA_CHOICES = ((3,'Mínima contaminación de cuerpos de agua naturales (probado con regularidad en la comunidad)'),
                            (2,'Pocos casos de contaminación y las medidas adoptadas para mejorar las condiciones'),
                            (1,'Casos frecuentes de contaminación, pero realizan pruebas del agua y toman medidas'),
                            (0,'Contaminación frecuente, sin agua y sin medidas para mejorar las condiciones')
                            )

class UsoEficienteAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    gestion_riesgo = models.IntegerField(choices = GESTION_CHOICES,verbose_name = '20.1 Gestión del riego')
    retencion_agua = models.IntegerField(choices = RETENCION_CHOICES,verbose_name = '20.2 Retención de agua y la escorrentía')
    eficiencia_agua = models.IntegerField(choices = EFICIENCIA_CHOICES,verbose_name = '20.3 Eficiencia del Agua (aplicable para el procesamiento)')
    contaminacion_agua = models.IntegerField(choices = CONTAMINACION_AGUA_CHOICES,verbose_name = '20.4 Contaminación del agua')

    class Meta:
        verbose_name_plural = '20. El uso eficiente del agua y calidad del agua'

PRUEBAS_CHOICES = ((3,'El análisis del suelo es realizado recientemente en terreno/Granja/FO nivel que sea homogéneo'),
                    (2,'Se realiza el análisis del suelo, pero los datos son mayores de 5 años y no refleja las condiciones no homogéneos'),
                    (1,'Los datos de análisis de suelo no está disponible pero se han tomado medidas para obtener datos de suelos'),
                    (0,'No se dispone de datos de pruebas del suelo y ninguna de las medidas adoptadas para obtener datos')
                    )

MANEJO_NUTRIENTES = ((3,'Manejo de nutrientes es altamente eficiente'),
                    (2,'Manejo de nutrientes es casi eficiente y toman medidas'),
                    (1,'Manejo de nutrientes es ineficiente, sino se toman medidas'),
                    (0,'Manejo de nutrientes es ineficaz sin las medidas adoptadas')
                    )

FERTILIZANTE_ORGANICO = ((3,'Se ha optimizado el uso de fertilizantes orgánicos'),
                        (2,'El uso de fertilizantes orgánicos es casi óptima con las medidas adoptadas'),
                        (1,'El uso de fertilizantes orgánicos está lejos de ser óptima con las medidas adoptadas'),
                        (0,'El uso de fertilizantes orgánicos está lejos de optimizar sin las medidas adoptadas')
                        )

BALANCE_CHOICES = ((2,'Balance de N y P en la granja se mantiene'),
                    (1,'N y P fuera de equilibrio con las medidas adoptadas'),
                    (0,'N y P gravemente desequilibrado, pero tomar contramedidas')
                    )

RESIDUOS_CHOICES = ((3,'Todos los pasos identificados han sido adoptados. No hay signos de botar o derrame'),
                    (2,'La gestión de los residuos en el lugar con medidas tomadas para mejorar aún más'),
                    (1,'Sin la gestión de los residuos , pero las medidas adoptadas'),
                    (0,'La gestión de residuos y sin ningún tipo de medidas')
                    )

ENVASES_CHOICES = ((3,'Agricultura orgánica sin dejar residuos, tales como contenedores de nocivos en el medio ambiente'),
                    (2,'Aplicación de un sistema para recoger, devolver o la eliminación segura de los envases de agroquímicos'),
                    (1,'Sin gestión de residuos agroquímicos, pero las medidas adoptadas'),
                    (0,'Sin gestión de residuos de agroquímicos y sin medidas')
                    )

PESTICIDA_CHOICES = ((3,'No se utilizan plaguicidas sintéticos'),
                    (2,'Se aplican los plaguicidas de baja toxicidad y minimizada en consonancia con las Buenas Prácticas Agrícolas (GAP) y el "2017 SAN'),
                    (1,'Gobierno nacional aprobó los plaguicidas se aplican según sus instrucciones de seguridad'),
                    (0,'Alta toxicidad o pesticidas ilegales son utilizados en forma no segura')
                    )

MIP_CHOICES = ((3,'MIP es la estrategia para el control de plagas'),
                (2,'MIP está parcialmente aplicada y control químico se combina con al menos dos métodos más'),
                (1,'MIP no se aplica todavía, pero el control químico es combinada con al menos un método más (biológicas, fisicas)'),
                (0,'El control de plagas se basa principalmente en el control químico (pesticidas sintéticos)')
                )

class GestionRecursosNaturales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    pruebas_suelo = models.IntegerField(choices = PRUEBAS_CHOICES,verbose_name = '21.1 Pruebas del suelo')
    manejo_nutrientes = models.IntegerField(choices = MANEJO_NUTRIENTES,verbose_name = '21.2 Manejo de nutrientes')
    fertilizante_organico = models.IntegerField(choices = FERTILIZANTE_ORGANICO,verbose_name = '21.3 Fertilizante orgánico')
    balance = models.IntegerField(choices = BALANCE_CHOICES,verbose_name = '21.4 Balance de nitrógeno y fósforo')
    gestion_residuos = models.IntegerField(choices = RESIDUOS_CHOICES,verbose_name = '21.5 Gestión de los residuos de la producción para procesar')
    gestion_envases = models.IntegerField(choices = ENVASES_CHOICES,verbose_name = '21.6 Gestión de envases vacíos de agroquímicos y productos agroquímicos sobrantes')
    uso_pesticida = models.IntegerField(choices = PESTICIDA_CHOICES,verbose_name = '21.7 Uso de pesticida')
    mip = models.IntegerField(choices = MIP_CHOICES,verbose_name = '21.8 MIP/MPN (Manejo integrado y gestión de plagas naturales)')

    class Meta:
        verbose_name_plural = '21. Gestión de recursos naturales'

EMISIONES_CARBONO = ((3,'Cero quema de materia orgánica en las granjas'),
                    (2,'Evidencia de baja emisión de carbono y se toman medidas'),
                    (1,'Altas y bajas emisiones de carbono, pero se han tomado medidas para mejorar'),
                    (0,'Alta y baja emisión de carbono sin que se tomen medidas')
                    )

PROCESAMIENTO_TRANSPORTE = ((3,'Productos transformados llegar al mercado con una óptima eficiencia de combustible'),
                            (2,'Los productos alcanzan el mercado estimado con alta eficiencia de combustible'),
                            (1,'Los productos llegan con baja eficiencia de uso de combustible pero adoptan medidas'),
                            (0,'Los productos llegan baja eficiencia de uso combustible (por vía aérea, ...) y no adoptan medidas')
                            )

class CambioClimatico(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    emision_carbono = models.IntegerField(choices = EMISIONES_CARBONO,verbose_name = '22.1 El carbono y el óxido nitroso (N2O): emisión de carbono +')
    procesamiento_transporte = models.IntegerField(choices = PROCESAMIENTO_TRANSPORTE,verbose_name = '22.2 Emisiones de Carbono: durante el procesamiento y transporte')

    class Meta:
        verbose_name_plural = '22. Cambio Climático'

DIVERSIDAD_VEGETAL = ((3,'La diversidad de especies vegetales está a un nivel óptimo'),
                        (2,'La diversidad vegetal debajo de una óptima con las medidas adoptadas'),
                        (1,'La diversidad de las especies vegetales a continuación óptima pero se toman medidas'),
                        (0,'Planta baja diversidad y ninguna de las medidas adoptadas')
                        )

DIVERSIDAD_GENETICA = ((3,'Sin el uso de Organismos genéticamente modificados / Transgénicos. La diversidad genética está aumentando'),
                        (2,'Sin el uso de Organismos genéticamente modificados / Transgénicos. La diversidad genética en la granja se mantiene y se adopten medidas para incrementar la diversidad'),
                        (1,'Se toman medidas para reducir el uso de los Organismos genéticamente modificados / Transgénicos. La diversidad genética en las explotaciones agrícolas está disminuyendo, pero se han tomado medidas'),
                        (0,'Uso intencional de Organismos genéticamente modificados / Transgénicos. No se adoptan medidas para aumentar la diversidad genética')
                        )
USO_TIERRA = ((3,'Ninguna destrucción de ecosistemas de gran valor desde 2014 y la conversión de ecosistemas naturales desde 2015'),
                (2,'No hay ninguna conversión de ecosistemas naturales desde 2015 y la compensación de las medidas adoptadas para la conversión anterior'),
                (1,'No hay ninguna conversión de ecosistemas naturales desde 2015 y sin compensación de las medidas adoptadas'),
                (0,'Conversión de ecosistemas naturales desde 2015')
                )

class Biodiversidad(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    diversidad_vegetal = models.IntegerField(choices = DIVERSIDAD_VEGETAL,verbose_name = '23.1 Diversidad vegetal')
    diversidad_genetica = models.IntegerField(choices = DIVERSIDAD_GENETICA,verbose_name = '23.2 Diversidad genética')
    uso_tierra = models.IntegerField(choices = USO_TIERRA,verbose_name = '23.3 El uso de la tierra y la conversión de la tierra')

    class Meta:
        verbose_name_plural = '23. Biodiversidad'

SALVAGUARDAR_ECOSISTEMAS = ((3,'Los ecosistemas naturales y sus valores de conectividad están aumentando'),
                            (2,'Los ecosistemas naturales están bien documentados y mantenidos. Las medidas adoptadas para mejorar el ecosistema de valores'),
                            (1,'Los ecosistemas naturales son mantenidas, pero ninguna de las medidas adoptadas para mejorar el ecosistema de valores'),
                            (0,'Los ecosistemas naturales y sus valores están disminuyendo. Ninguna de las medidas adoptadas para mejorar el ecosistema de valores')
                            )

VIDA_SILVESTRE = ((3,'No hay caza de animales silvestres'),
                    (2,'Caza legal sostenible a tarifa regulada'),
                    (1,'Caza legal pero no reglamentada'),
                    (0,'La caza ilegal o la caza en el ritmo insostenible')
                    )

TIERRAS_AGRICOLAS = ((3,'Utilización de las tierras agrícolas está en su óptimo definido localmente'),
                    (2,'Utilización de tierras agrícolas está por debajo de su óptimo definido localmente con las medidas adoptadas'),
                    (1,'Utilización de tierras agrícolas está por debajo de su óptimo definido localmente sin las medidas adoptadas'),
                    (0,'Tierras de cultivo no es apta para la agricultura')
                    )

ESPECIES_INVASORAS = ((3,'No existen especies invasoras'),
                    (2,'Sí hay especies invasoras, los agricultores adoptar contramedidas para reprimirlos'),
                    (1,'Los agricultores no son conscientes de los riesgos de las especies invasoras'),
                    (0,'Los agricultores son conscientes de especies invasoras, pero sin tomar medidas para suprimir la proliferación de especies invasoras')
                    )

class PaisajeSostenible(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    salvaguardar_ecosistemas = models.IntegerField(choices = SALVAGUARDAR_ECOSISTEMAS,verbose_name = '24.1 Salvaguardar los ecosistemas naturales + conectividad')
    proteccion_vida_silvestre = models.IntegerField(choices = VIDA_SILVESTRE,verbose_name = '24.2 Protección de la vida silvestre')
    tierras_agricolas = models.IntegerField(choices = TIERRAS_AGRICOLAS,verbose_name = '24.3 Uso óptimo de las tierras agrícolas')
    especies_invasoras = models.IntegerField(choices = ESPECIES_INVASORAS,verbose_name = '24.4 Especies invasoras')

    class Meta:
        verbose_name_plural = '24. Paisaje sostenible'

CULTIVOS_MIP = (('Cacao','Cacao'),('Café','Café'),('Hortalizas','Hortalizas'))

MATERIAL_CHOICES = ((1,'Material de siembra de buena calidad(libre de plagas y enfermedades)'),
                    (2,'Uso de variedades tolerantes,variedades mejoradas o criolla seleccionada'),
                    (3,'Uso de plántulas de calidad (Libre de plagas y enfermedades, vigorosas)'))

PREPARACION_TERRENO = ((1,'Acciones correctivas al suelo (Incorporación de cal o materia orgánica)'),
                        (2,'Preparación del terreno al menos 21 días antes de la siembra'),
                        (3,'Siembra con curvas a nivel o desnivel en terrenos con pendiente'),
                        (4,'Barreras vivas (Establecer Las 15-20 días antes de siembra o transplante)'),
                        (5,'Siembra en camas altas (mejor crecimiento radicular, absorción)'))

CONTROL_MALEZAS = ((1,'Control o pre germinación de malezas (15 días antes de la siembra o transplante)'),
                    (2,'Manejo de rondas'))

FERTILIZACION_ADECUADA = ((1,'Plan de fertilización según la demanda del cultivo'),
                            (2,'Uso de Solución Arrancadora'),
                            (3,'Fertilización diluida'))

DENSIDAD_SOMBRA = ((1,'Distanciamiento de planta adecuado'),
                    (2,'Densidad de planta adecuada'))

PLAGAS_ENFERMEDADES = ((1,'Muestreo de plagas de suelo al momento de la preparación del terreno'),
                        (2,'Control adecuado de plagas del suelo'),
                        (3,'Uso de insecticidas sistémicos como preventivo'),
                        (4,'Uso de Agribon en cultivos que lo ameriten'),
                        (5,'Uso de Trampas amarillas o pegajosas'),
                        (6,'Eliminación de plantas enfermas'),
                        (7,'Poda sanitaria en cultivos que así lo ameriten'),
                        (8,'Trampas olorosas'),
                        (9,'Uso de ácido salicílico o fosfonatos de potasio (Estimuladores de las defensas de la planta)'),
                        (10,'Eliminación de fruto dañado (gusanos, picudo)'),
                        (11,'Desinfección de estacas y mecates de amarres, si son reutilizados. En cultivos que necesiten tutoreo'),
                        (12,'Muestreo de plagas y enfermedades (AAE)'),
                        (13,'Uso de plástico de cobertura en cultivos que lo amerite'),
                        (14,'Control manual de plagas (larvas o huevos)'),
                        (15,'Utilización de equipos de protección para aplicación de plaguicidas'),
                        (16,'Utilización de productos coadyugantes (adherente, dispersables, penetrantes)'),
                        (17,'Calibración del equipo de aplicación'),
                        (18,'Utilización de productos biológicos'),
                        (19,'Eliminación inmediata de rastrojo'),
                        (20,'Rotación de cultivo'),
                        (21,'Regulación de pH de agua para la aplicación de plaguicidas, con un rango de pH de 5.5-7'),
                        )

class PracticasMIP(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.CharField(max_length = 50,choices = CULTIVOS_MIP)
    material_siembra_sano = MultiSelectField(choices = MATERIAL_CHOICES,verbose_name = 'Material de siembra sano',blank=True,null=True)
    preparacion_terreno = MultiSelectField(choices = PREPARACION_TERRENO,verbose_name = 'Preparación del Terreno',blank=True,null=True)
    control_malezas = MultiSelectField(choices = CONTROL_MALEZAS,verbose_name = 'Control de malezas',blank=True,null=True)
    fertilizacion_adecuada = MultiSelectField(choices = FERTILIZACION_ADECUADA,verbose_name = 'Fertilización Adecuada',blank=True,null=True)
    densidad_siembra = MultiSelectField(choices = DENSIDAD_SOMBRA,verbose_name = 'Densidad de siembra correcta',blank=True,null=True)
    control_plagas_enfermedades = MultiSelectField(choices = PLAGAS_ENFERMEDADES,verbose_name = 'Control de plagas y enfermedades',blank=True,null=True)

    class Meta:
        verbose_name_plural = 'VII. Prácticas MIP en la propiedad/finca'

@python_2_unicode_compatible
class PromedioNacional(models.Model):
    pais = models.ForeignKey(Pais)
    cultivo = models.IntegerField(choices = CULTIVO_CHOICES)

    def __str__(self):
        return '%s - %s' % (self.pais.nombre, self.get_cultivo_display())

    class Meta:
        verbose_name = 'Promedio Nacional'
        verbose_name_plural = 'Promedios Nacionales'

@python_2_unicode_compatible
class Promedio(models.Model):
    promedio_nacional = models.ForeignKey(PromedioNacional)
    anio = models.IntegerField()
    precio_promedio = models.FloatField()
    costo_promedio = models.FloatField()
    rendimiento_promedio = models.FloatField()
    ingreso_promedio = models.FloatField()

    def __str__(self):
        return '%s' % self.promedio_nacional

    class Meta:
        verbose_name = 'Promedio'
        verbose_name_plural = 'Promedios'
