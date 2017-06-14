# -*- coding: UTF-8 -*-
from django.db import models
from .models import *
from django import forms

def fecha_choice():
    years_evaluacion = []
    years_implementacion = []

    for en in ResultadosEvaluacion.objects.order_by('year').values_list('year', flat=True):
        years_evaluacion.append((en,en))

    for en in ResultadosImplementacion.objects.order_by('year').values_list('year', flat=True):
        years_implementacion.append((en,en))

    return list(sorted(set(years_evaluacion + years_implementacion)))

def organizaciones():
    org_evaluacion = []
    org_implementacion = []

    for org in ResultadosEvaluacion.objects.order_by('organizacion').distinct():
        org_evaluacion.append((org.id,org.organizacion.nombre))

    for org in ResultadosImplementacion.objects.order_by('organizacion').distinct():
        org_implementacion.append((org.id,org.organizacion.nombre))
    
    return list(sorted(set(org_evaluacion + org_implementacion)))


class OrganizacionesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrganizacionesForm, self).__init__(*args, **kwargs)
        self.fields['anio'] = forms.MultipleChoiceField(choices=fecha_choice(),required=True,label='Año')
        self.fields['organizacion'] = forms.MultipleChoiceField(choices=organizaciones(),required=False,label='Organización')
        self.fields['pais'] = forms.ModelChoiceField(queryset=Pais.objects.all(), required=True,label='País')
