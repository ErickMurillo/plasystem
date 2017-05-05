# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *
from nested_admin import NestedStackedInline,NestedTabularInline,NestedModelAdmin
from .forms import *

# Register your models here.
class MiembrosFamilia_Inline(admin.TabularInline):
    model = MiembrosFamilia
    max_num = 12
    extra = 1

class DuenoPropiedad_Inline(admin.TabularInline):
    model = DuenoPropiedad
    can_delete = False
    max_num = 1

class DuenoSi_Inline(admin.TabularInline):
    model = DuenoSi
    can_delete = False
    max_num = 1

class DuenoNo_Inline(admin.TabularInline):
    model = DuenoNo
    can_delete = False
    max_num = 1

class ProductorAdmin(admin.ModelAdmin):
    inlines = [MiembrosFamilia_Inline,DuenoPropiedad_Inline,DuenoSi_Inline,DuenoNo_Inline]

    class Media:
		js = ('js/admin.js',)

admin.site.register(Productor,ProductorAdmin)

class AreaFinca_Inline(NestedTabularInline):
    model = AreaFinca
    can_delete = False
    max_num = 1

class DistribucionFinca_Inline(NestedTabularInline):
    model = DistribucionFinca
    max_num = 7
    extra = 1

class Certificacion_Inline(NestedTabularInline):
    model = Certificacion
    can_delete = False
    max_num = 1

class TipoCertificacion_Inline(NestedTabularInline):
    model = TipoCertificacion
    can_delete = False
    max_num = 1

class CertificadoEmpresa_Inline(NestedTabularInline):
    model = CertificadoEmpresa
    can_delete = False
    max_num = 1

class BPAPregunta_Inline(NestedTabularInline):
    model = BPAPregunta
    can_delete = False
    max_num = 1

class BPA_Inline(NestedTabularInline):
    model = BPA
    can_delete = False
    max_num = 1

class Produccion_Inline(NestedTabularInline):
    model = Produccion
    extra = 1
    form = ProduccionForm

class Mercado_Inline(NestedTabularInline):
    model = Mercado
    extra = 1

class DestinoProduccion_Inline(NestedStackedInline):
    model = DestinoProduccion
    extra = 1
    inlines = [Mercado_Inline]

class IngresosOtrosCultivos_Inline(NestedTabularInline):
    model = IngresosOtrosCultivos
    extra = 1

class IngresosFamilia_Inline(NestedTabularInline):
    model = IngresosFamilia
    can_delete = False
    max_num = 1

class FuenteIngresos_Inline(NestedTabularInline):
    model = FuenteIngresos
    extra = 1

class IngresosActividadesGanaderia_Inline(NestedTabularInline):
    model = IngresosActividadesGanaderia
    extra = 1
    max_num = 3

class CondicionesRiegos_Inline(NestedTabularInline):
    model = CondicionesRiegos
    can_delete = False
    max_num = 1

class ConservacionSuelo_Inline(NestedStackedInline):
    model = ConservacionSuelo
    can_delete = False
    max_num = 1

class UsoEficienteAgua_Inline(NestedStackedInline):
    model = UsoEficienteAgua
    can_delete = False
    max_num = 1

class GestionRecursosNaturales_Inline(NestedStackedInline):
    model = GestionRecursosNaturales
    can_delete = False
    max_num = 1

class CambioClimatico_Inline(NestedStackedInline):
    model = CambioClimatico
    can_delete = False
    max_num = 1

class Biodiversidad_Inline(NestedStackedInline):
    model = Biodiversidad
    can_delete = False
    max_num = 1

class PaisajeSostenible_Inline(NestedStackedInline):
    model = PaisajeSostenible
    can_delete = False
    max_num = 1

class PracticasMIP_Inline(NestedStackedInline):
    model = PracticasMIP
    can_delete = False
    max_num = 1

class EncuestaAdmin(NestedModelAdmin):
    list_display = ('productor','encuestador','grupo','fecha')
    search_fields = ['productor__nombre','encuestador__nombre']
    list_filter = ('grupo',)
    date_hierarchy = 'fecha'

    inlines = [AreaFinca_Inline,DistribucionFinca_Inline,Certificacion_Inline,TipoCertificacion_Inline,
                CertificadoEmpresa_Inline,BPAPregunta_Inline,BPA_Inline,Produccion_Inline,DestinoProduccion_Inline,
                IngresosOtrosCultivos_Inline,IngresosFamilia_Inline,FuenteIngresos_Inline,
                IngresosActividadesGanaderia_Inline,CondicionesRiegos_Inline,ConservacionSuelo_Inline,
                UsoEficienteAgua_Inline,GestionRecursosNaturales_Inline,CambioClimatico_Inline,
                Biodiversidad_Inline,PaisajeSostenible_Inline,PracticasMIP_Inline]

    class Media:
        css = {'all': ('css/admin-encuesta.css','css/select2.min.css')}
        js = ('js/jquery.min.js','js/select2.min.js','js/encuesta-admin.js')

class CultivoAdmin(admin.ModelAdmin):
    list_filter = ('tipo',)
    search_fields = ('nombre',)

admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Encuestador)
admin.site.register(Certificado)
admin.site.register(EmpresaCertifica)
admin.site.register(EliminacionFocos)
admin.site.register(ProteccionFuentes)
admin.site.register(Cultivo,CultivoAdmin)
admin.site.register(TipoSistemaRiego)

class Promedio_Inline(admin.TabularInline):
    model = Promedio
    extra = 1
    form = PromedioForm

class PromedioNacionalAdmin(admin.ModelAdmin):
    inlines = [Promedio_Inline,]
    list_filter = ('pais','cultivo__tipo')
    search_fields = ('cultivo__nombre',)

admin.site.register(PromedioNacional,PromedioNacionalAdmin)
