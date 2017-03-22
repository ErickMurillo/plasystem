# -*- coding: utf-8 -*-
from django import forms
from .models import *

import datetime

ANIO_ACTUAL = datetime.datetime.today().year


def fecha_choice():
    years = []
    for en in range(int(ANIO_ACTUAL),int(ANIO_ACTUAL)+5):
        years.append((en,en))
    return sorted(list(set(years)))


class CustomChoiceField(forms.ChoiceField):

    def __init__(self, *args, **kwargs):
        super(CustomChoiceField, self).__init__(*args, **kwargs)
        self.choices.insert(0, (None , '--------'))


class RegistroMesesForm(forms.ModelForm):
    anios = CustomChoiceField(choices=fecha_choice())
    class Meta:
        model = RegistroMeses
        fields = '__all__'

class TasaCambioPaisAnualForm(forms.ModelForm):
    anio = CustomChoiceField(choices=fecha_choice())
    class Meta:
        model = TasaCambioPaisAnual
        fields = '__all__'