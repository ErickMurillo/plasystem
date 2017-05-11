# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class OrganizacionAdmin(admin.ModelAdmin):
	#fields = (('nombre', 'tipo'), 'direccion')
	# fields = (
	# 	('nombre', 'tipo', 'direccion'), 
	# 	('pais','departamento','municipio'),
	# 	('oficina_numero','oficina_correo','sitio_web'),
	# 	('red_social1','red_social2','red_social3','red_social4'),
	# 	('persona1_contacto','persona1_cargo','persona1_telefono','persona1_correo'),
	# 	('persona2_contacto','persona2_cargo','persona2_telefono','persona2_correo'),
	# 	)

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

# Register your models here.
admin.site.register(Organizacion, OrganizacionAdmin)
admin.site.register(TipoOrganizacion)
