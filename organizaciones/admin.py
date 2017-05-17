# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class ApoyoDonanteInline(admin.TabularInline):
    model = ApoyoDonante
    extra = 1

class OrganizacionPerteneceInline(admin.TabularInline):
    model = OrganizacionPertenece
    extra = 1

class MiembrosOficialesInline(admin.TabularInline):
    model = MiembrosOficiales
    extra = 1

class NumeroCooperativaInline(admin.TabularInline):
    model = NumeroCooperativa
    extra = 1

class ProductoresProveedoresInline(admin.TabularInline):
    model = ProductoresProveedores
    extra = 1

class EmpleadosOrganizacionInline(admin.TabularInline):
    model = EmpleadosOrganizacion
    extra = 1

class InfraestructuraInline(admin.TabularInline):
    model = Infraestructura
    extra = 1

class SectoresProductosInline(admin.TabularInline):
    model = SectoresProductos
    extra = 1

class ActividadInline(admin.TabularInline):
    model = Actividad
    extra = 1

class ServicioInline(admin.TabularInline):
    model = Actividad
    extra = 1

class OrganizacionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('nombre', 'tipo', 'direccion'),('pais',
                       'departamento','municipio'),('oficina_numero',
                       'oficina_correo'),'sitio_web')
        }),
        ('Redes Sociales', {
            'fields': (('red_social1','red_social2'),
                        ('red_social3','red_social4')),
        }),
        ('Persona de contacto 1', {
            'fields': (('persona1_contacto','persona1_cargo'),
                       ('persona1_telefono','persona1_correo')),
        }),
        ('Persona de contacto 2', {
            'fields': (('persona2_contacto','persona2_cargo'),
                      ('persona2_telefono','persona2_correo')),
        }),
        ('Situación legal y organizativa de la organización', {
            'fields': (('personeria','en_operaciones','incorporacion'),
                      ('licencia','tributaria'),'vision','mision','apoyo'),
        }),
    )
    inlines = [
               ApoyoDonanteInline,OrganizacionPerteneceInline,
               MiembrosOficialesInline,NumeroCooperativaInline,
               ProductoresProveedoresInline,EmpleadosOrganizacionInline,
               InfraestructuraInline,SectoresProductosInline,
               ActividadInline,ServicioInline
               ]


admin.site.register(Organizacion, OrganizacionAdmin)
admin.site.register(TipoOrganizacion)