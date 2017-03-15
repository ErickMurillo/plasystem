from django.contrib import admin

from .models import *

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

class AreaFinca_Inline(admin.TabularInline):
    model = AreaFinca
    can_delete = False
    max_num = 1

class DistribucionFinca_Inline(admin.TabularInline):
    model = DistribucionFinca
    max_num = 7
    extra = 1

class Certificacion_Inline(admin.TabularInline):
    model = Certificacion
    can_delete = False
    max_num = 1

class TipoCertificacion_Inline(admin.TabularInline):
    model = TipoCertificacion
    can_delete = False
    max_num = 1

class CertificadoEmpresa_Inline(admin.TabularInline):
    model = CertificadoEmpresa
    can_delete = False
    max_num = 1

class BPA_Inline(admin.TabularInline):
    model = BPA
    can_delete = False
    max_num = 1

class Produccion_Inline(admin.TabularInline):
    model = Produccion
    extra = 1

class EncuestaAdmin(admin.ModelAdmin):
    inlines = [AreaFinca_Inline,DistribucionFinca_Inline,Certificacion_Inline,TipoCertificacion_Inline,
                CertificadoEmpresa_Inline,BPA_Inline,Produccion_Inline]

    class Media:
		js = ('js/encuesta-admin.js',)

admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Encuestador)
admin.site.register(Certificado)
admin.site.register(EmpresaCertifica)
admin.site.register(EliminacionFocos)
admin.site.register(ProteccionFuentes)
admin.site.register(Cultivo)
