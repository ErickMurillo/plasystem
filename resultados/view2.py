from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from organizaciones.models import *
from django.db.models import Sum, Count, Avg, F
from resultados.models import *
import collections

from .views import _queryset_filtrado

def grafo_comparativo(request, template='resultados/grafo-resultado.html'):

    years = []
    for en in ResultadosEvaluacion.objects.order_by('year').values_list('year', flat=True):
        years.append((en,en))

    muchos_tiempo = list(sorted(set(years)))

    comparativa_dict = collections.OrderedDict()

    for anio in muchos_tiempo:
        bloque1 = GestionInterna.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque2 = Operaciones.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque3 = Sostenibilidad.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque4 = GestionFinanciera.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque5 = DesempenoFinanciero.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque6 = Suministros.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque7 = Mercados.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque8 = RiesgoExternos.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']
        bloque9 = Facilitadores.objects.filter(resultado__year=anio[0],opciones=1).aggregate(average=Avg('valor'))['average']


        comparativa_dict[anio[1]] = [bloque1,bloque2,bloque3,bloque4,bloque5,bloque6,
                                    bloque7,bloque8,bloque9]

    grafo_volumen = {}
    for obj in CHOICE_TIPO_MERCADO:
        valor = IncrementoAbastecimiento.objects.filter(tipo_mercado=obj[0]).count()
        if valor > 0:
            grafo_volumen[obj[1]] = valor


    years2 = []
    for en in ResultadosImplementacion.objects.order_by('year').values_list('year', flat=True):
        years2.append((en,en))

    grafo_incremento = {}
    for year in years2:
        for obj in CHOICE_AUMENTADO_INGRESOS:
            valor_hombre = AumentadoIngresos.objects.filter(resultado_implementacion__year=year[0],opcion=obj[0]).aggregate(hombre=Avg('cantidad_hombres'))['hombre']
            valor_mujer = AumentadoIngresos.objects.filter(resultado_implementacion__year=year[0],opcion=obj[0]).aggregate(mujer=Avg('cantidad_mujeres'))['mujer']
            suma_valores = valor_hombre + valor_mujer
            if suma_valores > 0:
                grafo_incremento[obj[1]] = suma_valores

    print grafo_incremento

    return render(request, template, {'comparativa':comparativa_dict,
                                      'grafo_volumen':grafo_volumen,
                                      'inicio_incremento':years2[0][0],
                                      'grafo_incremento':grafo_incremento})