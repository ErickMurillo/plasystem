from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TipoOrganizacion(models.Model):
    nombre = models.CharField(max_length = 200)

class Organizacion(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo = models.ForeignKey(TipoOrganizacion)
