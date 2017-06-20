# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline,NestedModelAdmin

class ApoyoDonanteInline(NestedTabularInline):
    model = ApoyoDonante
    extra = 1

class OrganizacionPerteneceInline(NestedTabularInline):
    model = OrganizacionPertenece
    max_num = 1

class MiembrosOficialesInline(NestedTabularInline):
    model = MiembrosOficiales
    extra = 1

class NumeroCooperativaInline(NestedTabularInline):
    model = NumeroCooperativa
    extra = 1

class ProductoresProveedoresInline(NestedTabularInline):
    model = ProductoresProveedores
    extra = 1

class EmpleadosOrganizacionInline(NestedTabularInline):
    model = EmpleadosOrganizacion
    extra = 1

class InfraestructuraInline(NestedTabularInline):
    model = Infraestructura
    extra = 1

class ProductosInline(NestedTabularInline):
    model = Productos
    extra = 1
    max_num = 5

class SectoresInline(NestedTabularInline):
    model = SectoresProductos
    extra = 1
    inlines = [ProductosInline]
    max_num = 4

class ActividadInline(NestedTabularInline):
    model = Actividad
    extra = 1

class ServicioInline(NestedTabularInline):
    model = Servicio
    extra = 1

class OrganizacionAdmin(NestedModelAdmin):
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
        ('II.Situación legal y organizativa de la organización', {
            'fields': (('personeria','en_operaciones','incorporacion'),
                      ('licencia','tributaria'),'vision','mision','apoyo'),
        }),
    )
    inlines = [
               ApoyoDonanteInline,OrganizacionPerteneceInline,
               MiembrosOficialesInline,NumeroCooperativaInline,
               ProductoresProveedoresInline,EmpleadosOrganizacionInline,
               InfraestructuraInline,SectoresInline,
               ActividadInline,ServicioInline
               ]


admin.site.register(Organizacion, OrganizacionAdmin)
admin.site.register(TipoOrganizacion)
admin.site.register(ApoyoDonante)
admin.site.register(Areas)
admin.site.register(Instituciones)
admin.site.register(ProductosOrg)