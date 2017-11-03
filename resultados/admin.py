from django.contrib import admin
from .models import *

class GestionInternaInline(admin.TabularInline):
    model = GestionInterna
    extra = 1
    max_num = 4

class OperacionesInline(admin.TabularInline):
    model = Operaciones
    extra = 1
    max_num = 4

class SostenibilidadInline(admin.TabularInline):
    model = Sostenibilidad
    extra = 1
    max_num = 3

class GestionFinancieraInline(admin.TabularInline):
    model = GestionFinanciera
    extra = 1
    max_num = 4

class DesempenoFinancieroInline(admin.TabularInline):
    model = DesempenoFinanciero
    extra = 1
    max_num = 4

class SuministrosInline(admin.TabularInline):
    model = Suministros
    extra = 1
    max_num = 6

class MercadosInline(admin.TabularInline):
    model = Mercados
    extra = 1
    max_num = 4

class RiesgoExternosInline(admin.TabularInline):
    model = RiesgoExternos
    extra = 1
    max_num = 5

class FacilitadoresInline(admin.TabularInline):
    model = Facilitadores
    extra = 1
    max_num = 6

class ResultadoEvaluacionAdmin(admin.ModelAdmin):
    inlines = [GestionInternaInline,OperacionesInline,
                SostenibilidadInline,GestionFinancieraInline,
                DesempenoFinancieroInline,SuministrosInline,
                MercadosInline,RiesgoExternosInline,FacilitadoresInline]
    class Media:
        css = {'all': ('css/admin-resultado-implementacion.css',)}

# Register your models here.
admin.site.register(Digitador)
admin.site.register(ResultadosEvaluacion, ResultadoEvaluacionAdmin)

class ProducenComercializanInline(admin.TabularInline):
    model = ProducenComercializan
    extra = 1
    max_num = 3

class AcuerdoComercialInline(admin.TabularInline):
    model = AcuerdoComercial
    extra = 1
    max_num = 1

class IncrementoAbastecimientoInline(admin.TabularInline):
    model = IncrementoAbastecimiento
    extra = 1

class AumentadoIngresosInline(admin.TabularInline):
    model = AumentadoIngresos
    extra = 1

#class AumentadoProductividadInline(admin.TabularInline):
#    model = AumentadoProductividad
#    extra = 1
#    max_num = 1

class ResultadosImplementacionAdmin(admin.ModelAdmin):
    inlines = [ProducenComercializanInline,AcuerdoComercialInline,
               IncrementoAbastecimientoInline,
               AumentadoIngresosInline]

    class Media:
        css = {'all': ('css/admin-resultado-implementacion.css',)}


admin.site.register(ResultadosImplementacion, ResultadosImplementacionAdmin)
