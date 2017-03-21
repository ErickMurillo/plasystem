from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Componentes)
admin.site.register(DatosGenerales)
admin.site.register(ObjetivosResultados)
admin.site.register(Indicadores)
admin.site.register(Aspectos)
admin.site.register(UmbrelaDesempeno)
#register for plan anual

class RegistroMesesInline(admin.TabularInline):
	model = RegistroMeses
	extra = 1

class RegistroPlanAnualAdmin(admin.ModelAdmin):
	inlines = [RegistroMesesInline]

admin.site.register(TipoItem)
admin.site.register(Actividades)
admin.site.register(CategoriaGastos)
admin.site.register(RegistroPlanAnual, RegistroPlanAnualAdmin)
admin.site.register(RegistroMeses)
