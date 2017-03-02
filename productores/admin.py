from django.contrib import admin

from .models import *

# Register your models here.
class DuenoSi_Inline(admin.TabularInline):
    model = DuenoSi
    can_delete = False
    max_num = 1

class DuenoNo_Inline(admin.TabularInline):
    model = DuenoNo
    can_delete = False
    max_num = 1

class ProductorAdmin(admin.ModelAdmin):
    inlines = [DuenoSi_Inline,DuenoNo_Inline]

    class Media:
		js = ('js/admin.js',)

admin.site.register(Productor,ProductorAdmin)
admin.site.register(Organizacion)
admin.site.register(TipoOrganizacion)
