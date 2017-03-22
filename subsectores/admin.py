from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline,NestedModelAdmin
from .forms import *

class IndicadoresInline(NestedTabularInline):
    model = Indicadores
    extra = 1

class ObjetivosInline(NestedTabularInline):
    model = ObjetivosResultados
    extra = 1
    inlines = [IndicadoresInline]

class DatosGeneralesAdmin(NestedModelAdmin):
    inlines = [ObjetivosInline]

    class Media:
    	css = {
            'all': ('css/subSectorAdmin.css',)
        }



class TasaCambioPaisAnualInline(admin.TabularInline):
	form = TasaCambioPaisAnualForm
	model = TasaCambioPaisAnual
	extra = 1

class TipoCambiosMonedaPaisAdmin(admin.ModelAdmin):
	inlines = [TasaCambioPaisAnualInline]

class TasaCambioPaisAnualAdmin(admin.ModelAdmin):
	form = TasaCambioPaisAnualForm

# Register your models here.
admin.site.register(Componentes)
admin.site.register(GruposMetas)
admin.site.register(DatosGenerales, DatosGeneralesAdmin)
admin.site.register(ObjetivosResultados)
admin.site.register(Indicadores)
admin.site.register(Monedas)
admin.site.register(TipoCambiosMonedaPais, TipoCambiosMonedaPaisAdmin)
admin.site.register(TasaCambioPaisAnual,TasaCambioPaisAnualAdmin)
#register for plan anual

class RegistroMesesInline(admin.TabularInline):
	form = RegistroMesesForm
	model = RegistroMeses
	extra = 1

class RegistroPlanAnualAdmin(admin.ModelAdmin):
	inlines = [RegistroMesesInline]


admin.site.register(Actividades)
admin.site.register(CategoriaGastos)
admin.site.register(RegistroPlanAnual, RegistroPlanAnualAdmin)
admin.site.register(RegistroMeses)
