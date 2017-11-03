from django.contrib import admin

from .models import *

# Register your models here.
class ReporteAdmin(admin.ModelAdmin):
	search_fields = ('titulo',)
	list_display = ('titulo','fecha_elaborado','donante','subsector','pais')

admin.site.register(Reporte,ReporteAdmin)