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

class IntervencionInline(NestedTabularInline):
    model = Intervenciones
    extra = 1
    inlines = [ObjetivosInline]


class DatosGeneralesAdmin(NestedModelAdmin):
    inlines = [IntervencionInline]
    list_display = ('nombre','fecha_inicio','fecha_finalizacion','pais','responsable')
    search_fields = ('nombre','responsable')
    list_filter = ('pais',)
    date_hierarchy = 'fecha_finalizacion'

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
admin.site.register(GruposMetas)
admin.site.register(DatosGenerales, DatosGeneralesAdmin)
#admin.site.register(ObjetivosResultados)
#admin.site.register(Indicadores)
admin.site.register(Monedas)
admin.site.register(TipoCambiosMonedaPais, TipoCambiosMonedaPaisAdmin)
#admin.site.register(TasaCambioPaisAnual,TasaCambioPaisAnualAdmin)
#register for plan anual

class RegistroMesesInline(admin.TabularInline):
    form = RegistroMesesForm
    model = RegistroMeses
    extra = 1
    max_num = 4

class RegistroPlanAnualAdmin(admin.ModelAdmin):
    inlines = [RegistroMesesInline]
    list_display = ('proyecto','nombre','mostrar_informe_url')

    def mostrar_informe_url(self, obj):
        return '<a href="/ver/plan/%s">Ver Informe</a>' % (obj.proyecto.id)
    mostrar_informe_url.allow_tags = True

    # def save_model(self, request, obj, form, change):
    #     print "el save model"

    # def save_formset(self, request, form, formset, change):
    #     print "save model children"
    #     formset.save() # this will save the children
    #     form.instance.save() # form.instance is the parent

admin.site.register(CategoriaGastos)
admin.site.register(RegistroPlanAnual, RegistroPlanAnualAdmin)
admin.site.register(InformeMensual)
