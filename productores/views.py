# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import json as simplejson
from django.db.models import Sum, Count, Avg, F
import collections
from django.db.models import Q
from subsectores.models import *

# Create your views here.
def _queryset_filtrado(request):
    params = {}

    if request.session['anio']:
        params['anio__in'] = request.session['anio']

    if request.session['pais']:
        params['productor__pais'] = request.session['pais']

    if request.session['departamento']:
        params['productor__departamento__in'] = request.session['departamento']

    if request.session['municipio']:
        params['productor__municipio__in'] = request.session['municipio']

    if request.session['organizacion']:
        params['productor__organizacion__in'] = request.session['organizacion']

    if request.session['sexo']:
        params['productor__sexo'] = request.session['sexo']

    if request.session['edad']:
        params['productor__edad'] = request.session['edad']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

    return Encuesta.objects.filter(**params)

@login_required
def consulta_productores(request,template="productores/consulta.html"):
    if request.method == 'POST':
        mensaje = None
        form = ProductoresForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

            return HttpResponseRedirect('/productores/dashboard/')
        else:
            centinela = 0

    else:
        form = ProductoresForm()
        mensaje = "Existen alguno errores"
        try:
            del request.session['anio']
            del request.session['pais']
            del request.session['departamento']
            del request.session['municipio']
            del request.session['organizacion']
            del request.session['sexo']
            del request.session['edad']
        except:
            pass

    return render(request, template, locals())

def anios_encuesta(valor):
    years = []
    for en in Encuesta.objects.filter(productor__pais=valor).order_by('anio').values_list('anio', flat=True):
        years.append(en)
    return list(sorted(set(years)))

@login_required
def dashboard_productores(request,template="productores/dashboard.html"):
    if request.method == 'POST':
        mensaje = None
        form = ProductoresForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

        else:
            centinela = 0
    else:
        form = ProductoresForm()
        mensaje = "Existen alguno errores"

    if 'anio' not in request.session:
        if request.GET.get('pais', ''):
            id_pais = request.GET.get('pais', '')
            filtro = Encuesta.objects.filter(productor__pais = id_pais)
            years = anios_encuesta(id_pais)
    else:
        filtro = _queryset_filtrado(request)
        years1 = request.session['anio']
        years = map(int, years1)
        id_pais = request.session['pais'].id

    hectarea = 0.7050

    #conteos generales
    familias = filtro.distinct().count()
    hombres = filtro.filter(productor__sexo = 'Hombre').count()
    mujeres = filtro.filter(productor__sexo = 'Mujer').count()
    menores_35 = filtro.filter(productor__edad = 1).count()
    manzanas = filtro.aggregate(total = Avg('areafinca__area'))['total']
    try:
        hectareas = manzanas * hectarea
    except:
        hectareas = 0

    certificacion = filtro.filter(certificacion__certificacion = 'Si').count()

    #graficas
    anios = collections.OrderedDict()
    last_year = years[-1]
    rendimientos = collections.OrderedDict()
    ingresos_cafe = collections.OrderedDict()
    ingresos_cacao = collections.OrderedDict()
    ingresos_hostalizas = collections.OrderedDict()
    for year in years:
        tipo_cambio = TasaCambioPaisAnual.objects.filter(tipo_cambio__pais = id_pais,anio = year).values_list('dolar',flat = True)
        #ingresos
        cafe = filtro.filter(destinoproduccion__cultivo__tipo = 1, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        #convercion a dolares
        try:
            cafe = cafe / tipo_cambio[0]
        except:
            pass

        cacao = filtro.filter(destinoproduccion__cultivo__tipo = 2, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        try:
            cacao = cacao / tipo_cambio[0]
        except:
            pass

        hortalizas = filtro.filter(destinoproduccion__cultivo__tipo = 3, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        try:
            hortalizas = hortalizas / tipo_cambio[0]
        except:
            pass

        #indice de produccio sustentable
        #conservacion suelo
        try:
            conservacion_suelo = ((filtro.filter(anio = year).aggregate(total = Avg(F('conservacionsuelo__erosion')
                                    + F('conservacionsuelo__sanilizacion')
                                    + F('conservacionsuelo__contaminacion_suelo')
                                    + F('conservacionsuelo__materia_organica')))['total']) / 12) * 100
        except:
            conservacion_suelo = 0

        #uso_eficiente_agua
        try:
            uso_eficiente_agua = ((filtro.filter(anio = year).aggregate(total = Avg(F('usoeficienteagua__gestion_riesgo')
                                    + F('usoeficienteagua__retencion_agua')
                                    + F('usoeficienteagua__eficiencia_agua')
                                    + F('usoeficienteagua__contaminacion_agua')))['total']) / 12) * 100
        except:
            uso_eficiente_agua = 0

        #gestion_recursos_naturales
        try:
            gestion_recursos_naturales = ((filtro.filter(anio = year).aggregate(total = Avg(F('gestionrecursosnaturales__pruebas_suelo')
                                    + F('gestionrecursosnaturales__manejo_nutrientes')
                                    + F('gestionrecursosnaturales__fertilizante_organico')
                                    + F('gestionrecursosnaturales__balance')
                                    + F('gestionrecursosnaturales_gestion_residuos')
                                    + F('gestionrecursosnaturales__gestion_envases')
                                    + F('gestionrecursosnaturales__uso_pesticida')
                                    + F('gestionrecursosnaturales__mip')))['total']) / 23) * 100
        except:
            gestion_recursos_naturales = 0

        #cambio_climatico
        try:
            cambio_climatico = ((filtro.filter(anio = year).aggregate(total = Avg(F('cambioclimatico__emision_carbono')
                                    + F('cambioclimatico__procesamiento_transporte')))['total']) / 6) * 100
        except:
            cambio_climatico = 0

        #biodiversidad
        try:
            biodiversidad = ((filtro.filter(anio = year).aggregate(total = Avg(F('biodiversidad__diversidad_vegetal')
                                    + F('biodiversidad__diversidad_genetica')
                                    + F('biodiversidad__uso_tierra')))['total']) / 9) * 100
        except:
            biodiversidad = 0

        #paisaje_sostenible
        try:
            paisaje_sostenible = ((filtro.filter(anio = year).aggregate(total = Avg(F('paisajsostenible__salvaguardar_ecosistemas')
                                    + F('paisajesostenible__proteccion_vida_silvestre')
                                    + F('paisajesostenible__tierras_agricolas')
                                    + F('paisajesostenible__especies_invasoras')))['total']) / 12) * 100
        except:
            paisaje_sostenible = 0

        if year == years[-1]:
            #indice total produccion sustentable -------------------------------------------------
            indice = (conservacion_suelo + uso_eficiente_agua + gestion_recursos_naturales
                        + cambio_climatico + paisaje_sostenible) / 5

        # grafica Aumento del indice de manejo de plaga
        encuestas = filtro.filter(anio = year).count()
        cultivos = collections.OrderedDict()
        dicc_indice = collections.OrderedDict()
        for obj in CULTIVOS_MIP:
            total_material = 0
            for x in MATERIAL_CHOICES:
                material_siembra_sano = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__material_siembra_sano__icontains = x[0]).count()
                total_material = total_material + material_siembra_sano
            try:
                total_material = (total_material / float(encuestas)) * 33.33
            except:
                total_material = 0

            total_preparacion = 0
            for x in PREPARACION_TERRENO:
                preparacion_terreno = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__preparacion_terreno__icontains = x[0]).count()
                total_preparacion = total_preparacion + preparacion_terreno
            try:
                total_preparacion = (total_preparacion / float(encuestas)) * 20
            except:
                total_preparacion = 0

            total_control = 0
            for x in CONTROL_MALEZAS:
                control_malezas = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__control_malezas__icontains = x[0]).count()
                total_control = total_control + control_malezas
            try:
                total_control = (total_control / float(encuestas)) * 50
            except:
                total_control = 0

            total_fertilizacion = 0
            for x in FERTILIZACION_ADECUADA:
                fertilizacion_adecuada = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__fertilizacion_adecuada__icontains = x[0]).count()
                total_fertilizacion = total_fertilizacion + fertilizacion_adecuada
            try:
                total_fertilizacion = (total_fertilizacion / float(encuestas)) * 33.33
            except:
                total_fertilizacion = 0

            total_densidad = 0
            for x in DENSIDAD_SOMBRA:
                densidad_siembra = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__densidad_siembra__icontains = x[0]).count()
                total_densidad = total_densidad + densidad_siembra
            try:
                total_densidad = (total_densidad / float(encuestas)) * 50
            except:
                total_densidad = 0

            total_plagas = 0
            for x in DENSIDAD_SOMBRA:
                control_plagas_enfermedades = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__control_plagas_enfermedades__icontains = x[0]).count()
                total_plagas = total_plagas + control_plagas_enfermedades
            try:
                total_plagas = (total_plagas / float(encuestas)) * 50
            except:
                total_plagas = 0

            cultivos[obj[0]] = (total_material,total_preparacion,total_control,
                                total_fertilizacion,total_densidad,total_plagas)

            if year == years[-1]:
                total_indice = (total_material + total_preparacion + total_control
                                + total_fertilizacion + total_densidad + total_plagas) / 6
                dicc_indice[obj[0]] = (total_indice,years[-1])

        #distribucion de las areas
        areas = collections.OrderedDict()
        for obj in CULTIVO_CHOICES:
            area = filtro.filter(anio = year, produccion__cultivo__tipo = obj[0]).aggregate(
                    sembrada = Sum(F('produccion__area_sembrada') * hectarea),cosechada = Sum(F('produccion__area_cosechada') * hectarea))
            areas[obj[1]] = (area['sembrada'],area['cosechada'])

        #Cantidad de productores con produccion sustentable, practicas MIP y BPA --------------------------------------
        bpa = filtro.filter(anio = year, bpapregunta__respuesta = 'Si').count()

        mip = filtro.filter(Q(practicasmip__material_siembra_sano__isnull = False) |
                            Q(practicasmip__preparacion_terreno__isnull = False) |
                            Q(practicasmip__control_malezas__isnull = False) |
                            Q(practicasmip__fertilizacion_adecuada__isnull = False) |
                            Q(practicasmip__densidad_siembra__isnull = False) |
                            Q(practicasmip__control_plagas_enfermedades__isnull = False),
                            anio = year).count()

        l = [1,2,3]
        prod_sustentable = filtro.filter(Q(conservacionsuelo__erosion__in = l) |
                                        Q(conservacionsuelo__sanilizacion__in = l) |
                                        Q(conservacionsuelo__contaminacion_suelo__in = l) |
                                        Q(conservacionsuelo__materia_organica__in = l) |
                                        Q(usoeficienteagua__gestion_riesgo__in = l) |
                                        Q(usoeficienteagua__retencion_agua__in = l) |
                                        Q(usoeficienteagua__eficiencia_agua__in = l) |
                                        Q(gestionrecursosnaturales__pruebas_suelo__in = l) |
                                        Q(gestionrecursosnaturales__manejo_nutrientes__in = l) |
                                        Q(gestionrecursosnaturales__fertilizante_organico__in = l) |
                                        Q(gestionrecursosnaturales__balance__in = l) |
                                        Q(gestionrecursosnaturales__gestion_residuos__in = l) |
                                        Q(gestionrecursosnaturales__gestion_envases__in = l) |
                                        Q(gestionrecursosnaturales__uso_pesticida__in = l) |
                                        Q(gestionrecursosnaturales__mip__in = l) |
                                        Q(cambioclimatico__emision_carbono__in = l) |
                                        Q(cambioclimatico__procesamiento_transporte__in = l) |
                                        Q(biodiversidad__diversidad_vegetal__in = l) |
                                        Q(biodiversidad__diversidad_genetica__in = l) |
                                        Q(biodiversidad__uso_tierra__in = l) |
                                        Q(paisajesostenible__salvaguardar_ecosistemas__in = l) |
                                        Q(paisajesostenible__proteccion_vida_silvestre__in = l) |
                                        Q(paisajesostenible__tierras_agricolas__in = l) |
                                        Q(paisajesostenible__especies_invasoras__in = l),
                                        anio = year).count()

        #agregando al dic general por anio
        anios[year] = (cafe,cacao,hortalizas,conservacion_suelo,uso_eficiente_agua,gestion_recursos_naturales,
                        cambio_climatico,biodiversidad,paisaje_sostenible,cultivos,areas,prod_sustentable,mip,bpa)

        if encuestas >= 1:
            cafe_area_cosechada = filtro.filter(produccion__cultivo__tipo=1,
                                            anio=year).aggregate(t=Sum('produccion__area_cosechada'))['t']
            cafe_cantidad = filtro.filter(produccion__cultivo__tipo=1,
                                            anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
            try:
                rendimiento_cafe = float(cafe_cantidad) / float(cafe_area_cosechada)
            except:
                rendimiento_cafe = 0

            rendimiento_cafe_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=1).aggregate(t=Sum('rendimiento_promedio'))['t']


            #rendimento cacao
            cacao_area_cosechada = filtro.filter(produccion__cultivo__tipo=2,
                                            anio=year).aggregate(t=Sum('produccion__area_cosechada'))['t']
            cacao_cantidad = filtro.filter(produccion__cultivo__tipo=2,
                                            anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
            try:
                rendimiento_cacao = float(cacao_cantidad) / float(cacao_area_cosechada)
            except:
                rendimiento_cacao = 0

            rendimiento_cacao_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=2).aggregate(t=Sum('rendimiento_promedio'))['t']


            #rendiminetos hortaliza
            hortaliza_area_cosechada = filtro.filter(produccion__cultivo__tipo=3,
                                            anio=year).aggregate(t=Sum('produccion__area_cosechada'))['t']
            hortaliza_cantidad = filtro.filter(produccion__cultivo__tipo=3,
                                            anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
            try:
                rendimiento_hortaliza = float(hortaliza_cantidad) / float(hortaliza_area_cosechada)
            except:
                rendimiento_hortaliza = 0

            rendimiento_hortaliza_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=3).aggregate(t=Sum('rendimiento_promedio'))['t']

            rendimientos[year] = (rendimiento_cafe,rendimiento_cafe_nacional,
                                  rendimiento_cacao,rendimiento_cacao_nacional,
                                  rendimiento_hortaliza,rendimiento_hortaliza_nacional)

            #ingresos numero 13 en la encuesta cafe
            cafe_ingreso = Mercado.objects.filter(destino_produccion__encuesta__in=filtro,
                                                  destino_produccion__cultivo__tipo=1,
                                                  destino_produccion__encuesta__anio=year).aggregate(t=Sum('ingreso'))['t']

            try:
                cafe_ingreso = cafe_ingreso / tipo_cambio[0]
            except:
                pass

            cafe_ingreso_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=1).aggregate(t=Sum('ingreso_promedio'))['t']

            try:
                cafe_ingreso_nacional = cafe_ingreso_nacional / tipo_cambio[0]
            except:
                pass

            #costo viene numero 12 de la encuesta
            cafe_costo = filtro.filter(produccion__cultivo__tipo=1,
                                       anio=year).aggregate(t=Sum('produccion__costo_produccion'))['t'] + \
                         filtro.filter(produccion__cultivo__tipo=1,anio=year).aggregate(t=Sum('produccion__costo_inversion'))['t']

            try:
                cafe_costo = cafe_costo / tipo_cambio[0]
            except:
                pass

            cafe_costo_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=1).aggregate(t=Sum('costo_promedio'))['t']

            try:
                cafe_costo_nacional = cafe_costo_nacional / tipo_cambio[0]
            except:
                pass

            #margen cafe
            cafe_margen = cafe_ingreso - cafe_costo

            ingresos_cafe[year] = (cafe_ingreso,cafe_ingreso_nacional,
                              cafe_costo,cafe_costo_nacional,cafe_margen)
            #ingresos numero 13 en la encuesta cacao
            cacao_ingreso = Mercado.objects.filter(destino_produccion__encuesta__in=filtro,
                                                  destino_produccion__cultivo__tipo=2,
                                                  destino_produccion__encuesta__anio=year).aggregate(t=Sum('ingreso'))['t']

            try:
                cacao_ingreso = cacao_ingreso / tipo_cambio[0]
            except:
                pass

            cacao_ingreso_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=2).aggregate(t=Sum('ingreso_promedio'))['t']

            try:
                cacao_ingreso_nacional = cacao_ingreso_nacional / tipo_cambio[0]
            except:
                pass

            #costo viene numero 12 de la encuesta
            cacao_costo = filtro.filter(produccion__cultivo__tipo=2,
                                       anio=year).aggregate(t=Sum('produccion__costo_produccion'))['t'] + \
                        filtro.filter(produccion__cultivo__tipo=2,
                                       anio=year).aggregate(t=Sum('produccion__costo_inversion'))['t']

            try:
                cacao_costo = cacao_costo / tipo_cambio[0]
            except:
                pass

            cacao_costo_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=2).aggregate(t=Sum('costo_promedio'))['t']

            try:
                cacao_costo_nacional = cacao_costo_nacional / tipo_cambio[0]
            except:
                pass

            #margen cacao
            if cacao_ingreso == None:
                cacao_ingreso = 0
            cacao_margen = cacao_ingreso - cacao_costo
            ingresos_cacao[year] = (cacao_ingreso,cacao_ingreso_nacional,
                              cacao_costo,cacao_costo_nacional,cacao_margen)

            #ingresos numero 13 en la encuesta hortaliza
            hortaliza_ingreso = Mercado.objects.filter(destino_produccion__encuesta__in=filtro,
                                                  destino_produccion__cultivo__tipo=3,
                                                  destino_produccion__encuesta__anio=year).aggregate(t=Sum('ingreso'))['t']
            try:
                hortaliza_ingreso = hortaliza_ingreso / tipo_cambio[0]
            except:
                pass

            hortaliza_ingreso_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=3).aggregate(t=Sum('ingreso_promedio'))['t']

            try:
                hortaliza_ingreso_nacional = hortaliza_ingreso_nacional / tipo_cambio[0]
            except:
                pass

            #costo viene numero 12 de la encuesta
            hortaliza_costo = filtro.filter(produccion__cultivo__tipo=3,
                                       anio=year).aggregate(t=Sum('produccion__costo_produccion'))['t'] + \
                        filtro.filter(produccion__cultivo__tipo=3,
                                       anio=year).aggregate(t=Sum('produccion__costo_inversion'))['t']

            try:
                hortaliza_costo = hortaliza_costo / tipo_cambio[0]
            except:
                pass

            hortaliza_costo_nacional = Promedio.objects.filter(anio=year,
                                                    promedio_nacional__pais__id=id_pais,
                                                    promedio_nacional__cultivo=3).aggregate(t=Sum('costo_promedio'))['t']

            try:
                hortaliza_costo_nacional = hortaliza_costo_nacional / tipo_cambio[0]
            except:
                pass

            #margen hortaliza
            if hortaliza_ingreso == None:
                hortaliza_ingreso = 0
            hortaliza_margen = hortaliza_ingreso - hortaliza_costo
            ingresos_hostalizas[year] = (hortaliza_ingreso,hortaliza_ingreso_nacional,
                          hortaliza_costo,hortaliza_costo_nacional,hortaliza_margen)


    return render(request, template, locals())

@login_required
def distribucion_areas(request,template="productores/distribucion_areas.html"):
    if request.method == 'POST':
        mensaje = None
        form = ProductoresForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

        else:
            centinela = 0
    else:
        form = ProductoresForm()
        mensaje = "Existen alguno errores"

    if 'anio' not in request.session:
        if request.GET.get('pais', ''):
            id_pais = request.GET.get('pais', '')
            filtro = Encuesta.objects.filter(productor__pais = id_pais)
            years = anios_encuesta(id_pais)
    else:
        filtro = _queryset_filtrado(request)
        years = request.session['anio']

    hectarea = 0.7050

    #conteos generales
    productores = filtro.distinct()
    familias = productores.count()
    hombres = filtro.filter(productor__sexo = 'Hombre').count()
    mujeres = filtro.filter(productor__sexo = 'Mujer').count()
    menores_35 = filtro.filter(productor__edad = 1).count()
    manzanas = filtro.aggregate(total = Avg('areafinca__area'))['total']
    try:
        hectareas = manzanas * hectarea
    except:
        hectareas = 0

    certificacion = filtro.filter(certificacion__certificacion = 'Si').count()

    #grafico de distribucion
    distribucion = collections.OrderedDict()
    for obj in DISTRIBUCION_CHOICES:
        promedio_area = filtro.filter(distribucionfinca__seleccion = obj[0]).aggregate(avg = Avg('distribucionfinca__cantidad'))['avg']
        distribucion[obj[0]] = promedio_area

    return render(request, template, locals())

@login_required
def ficha_productor(request,id=None,template="productores/ficha_productor.html"):
    if request.method == 'POST':
        mensaje = None
        form = ProductoresForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

        else:
            centinela = 0
    else:
        form = ProductoresForm()
        mensaje = "Existen alguno errores"

    if 'anio' not in request.session:
        if request.GET.get('pais', ''):
            id_pais = request.GET.get('pais', '')
            filtro = Encuesta.objects.filter(productor__pais = id_pais)
            years = anios_encuesta(id_pais)
    else:
        filtro = _queryset_filtrado(request)
        years = request.session['anio']
        id_pais = request.session['pais'].id

    hectarea = 0.7050

    #conteos generales
    familias = filtro.distinct().count()
    hombres = filtro.filter(productor__sexo = 'Hombre').count()
    mujeres = filtro.filter(productor__sexo = 'Mujer').count()
    menores_35 = filtro.filter(productor__edad = 1).count()
    manzanas = filtro.aggregate(total = Avg('areafinca__area'))['total']
    try:
        hectareas = manzanas * hectarea
    except:
        hectareas = 0

    certificacion = filtro.filter(certificacion__certificacion = 'Si').count()

    #-----------------------------------------------
    productor = Productor.objects.get(id = id)
    today = date.today()
    edad = today.year - productor.fecha_naciemiento.year - ((today.month, today.day) < (productor.fecha_naciemiento.month, productor.fecha_naciemiento.day))

    anios = collections.OrderedDict()
    for year in years:
        distribucion = collections.OrderedDict()
        for obj in DISTRIBUCION_CHOICES:
            area = DistribucionFinca.objects.filter(encuesta__anio = year,encuesta__productor = productor, seleccion = obj[0]).values_list('cantidad', flat=True)
            distribucion[obj[0]] = area

        tipo_cambio = TasaCambioPaisAnual.objects.filter(tipo_cambio__pais = id_pais,anio = year).values_list('dolar',flat = True)
        ingresos
        cafe = DestinoProduccion.objects.filter(encuesta__productor = productor, cultivo__tipo = 1, encuesta__anio = year).aggregate(
                sum = Sum(F('mercado__cantidad') * F('mercado__precio')))['sum']

        #convercion a dolares
        try:
            cafe = cafe / tipo_cambio[0]
        except:
            pass

        cacao = DestinoProduccion.objects.filter(encuesta__productor = productor, cultivo__tipo = 2, encuesta__anio = year).aggregate(
                sum = Sum(F('mercado__cantidad') * F('mercado__precio')))['sum']

        try:
            cacao = cacao / tipo_cambio[0]
        except:
            pass

        hortalizas = DestinoProduccion.objects.filter(encuesta__productor = productor, cultivo__tipo = 3, encuesta__anio = year).aggregate(
                sum = Sum(F('mercado__cantidad') * F('mercado__precio')))['sum']

        try:
            hortalizas = hortalizas / tipo_cambio[0]
        except:
            pass

        anios[year] = (distribucion,cafe,cacao,hortalizas)
    return render(request, template, locals())

@login_required
def ingresos(request,template="productores/ingresos.html"):
    if request.method == 'POST':
        mensaje = None
        form = ProductoresForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad'] = form.cleaned_data['edad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

        else:
            centinela = 0
    else:
        form = ProductoresForm()
        mensaje = "Existen alguno errores"

    if 'anio' not in request.session:
        if request.GET.get('pais', ''):
            id_pais = request.GET.get('pais', '')
            filtro = Encuesta.objects.filter(productor__pais = id_pais)
            years = anios_encuesta(id_pais)
    else:
        filtro = _queryset_filtrado(request)
        years = request.session['anio']
        id_pais = request.session['pais'].id

    hectarea = 0.7050

    #conteos generales
    productores = filtro.distinct()
    familias = productores.count()
    hombres = filtro.filter(productor__sexo = 'Hombre').count()
    mujeres = filtro.filter(productor__sexo = 'Mujer').count()
    menores_35 = filtro.filter(productor__edad = 1).count()
    manzanas = filtro.aggregate(total = Avg('areafinca__area'))['total']
    try:
        hectareas = manzanas * hectarea
    except:
        hectareas = 0

    certificacion = filtro.filter(certificacion__certificacion = 'Si').count()

    #graficos
    anios = collections.OrderedDict()
    for year in years:
        tipo_cambio = TasaCambioPaisAnual.objects.filter(tipo_cambio__pais = id_pais,anio = year).values_list('dolar',flat = True)

        merc_formal = ['Empresas comercializadoras','Empresas procesadoras',
                        'Empresas exportadoras','Supermercados','Cadena de restaurantes']

        merc_informal = ['Mercado tradicional','Cooperativa','Ferias','Intermediarios']

        cultivos = collections.OrderedDict()
        for obj in CULTIVO_CHOICES:
            ventas_formal = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = obj[0],
                                        destinoproduccion__mercado__mercado__in = merc_formal).aggregate(
                                        ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

            ventas_informal = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = obj[0],
                                        destinoproduccion__mercado__mercado__in = merc_informal).aggregate(
                                        ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

            cultivos[obj[1]] = (ventas_formal,ventas_informal)

        ventas = collections.OrderedDict()
        for mercado in MERCADO_CHOICES:
            cafe = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 1,
                                destinoproduccion__mercado__mercado = mercado[0]).aggregate(
                                ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

            cacao = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 2,
                                destinoproduccion__mercado__mercado = mercado[0]).aggregate(
                                ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

            hortalizas = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 3,
                                destinoproduccion__mercado__mercado = mercado[0]).aggregate(
                                ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

            ventas[mercado[0]] = cafe,cacao,hortalizas

        #grafica 5 incremento del vol de prod
        #cafe
        cafe_prod = filtro.filter(anio = year,produccion__cultivo__tipo = 1).aggregate(prod = Sum(
                                    'produccion__cantidad_cosechada'))['prod']

        try:
            area_cafe = (filtro.filter(produccion__cultivo__tipo = 1,anio=year).aggregate(
                                                t = Sum('produccion__area_cosechada'))['t']) * hectarea
        except:
            area_cafe = 0


        try:
            sembrada_cafe = (filtro.filter(produccion__cultivo__tipo = 1,anio=year).aggregate(
                                                t = Sum('produccion__area_sembrada'))['t']) * hectarea
        except:
            sembrada_cafe = 0

        cantidad_cafe = filtro.filter(produccion__cultivo__tipo = 1,
                                        anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
        try:
            rendimiento_cafe = float(cantidad_cafe) / float(area_cafe)
        except:
            rendimiento_cafe = 0

        #cacao
        cacao_prod = filtro.filter(anio = year,produccion__cultivo__tipo = 2).aggregate(prod = Sum(
                                    'produccion__cantidad_cosechada'))['prod']

        try:
            area_cacao = (filtro.filter(produccion__cultivo__tipo = 2,anio=year).aggregate(
                                                t = Sum('produccion__area_cosechada'))['t']) * hectarea
        except:
            area_cacao = 0


        try:
            sembrada_cacao = (filtro.filter(produccion__cultivo__tipo = 2,anio=year).aggregate(
                                                t = Sum('produccion__area_sembrada'))['t']) * hectarea
        except:
            sembrada_cacao = 0

        cantidad_cacao = filtro.filter(produccion__cultivo__tipo = 2,
                                        anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
        try:
            rendimiento_cacao = float(cantidad_cacao) / float(area_cacao)
        except:
            rendimiento_cacao = 0

        #hortaliza
        hortaliza_prod = filtro.filter(anio = year,produccion__cultivo__tipo = 3).aggregate(prod = Sum(
                                    'produccion__cantidad_cosechada'))['prod']

        try:
            area_hortaliza = (filtro.filter(produccion__cultivo__tipo = 3,anio=year).aggregate(
                                                t = Sum('produccion__area_cosechada'))['t']) * hectarea
        except:
            area_hortaliza = 0

        try:
            sembrada_hortaliza = (filtro.filter(produccion__cultivo__tipo = 3,anio=year).aggregate(
                                                t = Sum('produccion__area_sembrada'))['t']) * hectarea
        except:
            sembrada_hortaliza = 0

        cantidad_hortaliza = filtro.filter(produccion__cultivo__tipo = 3,
                                        anio=year).aggregate(t=Sum('produccion__cantidad_cosechada'))['t']
        try:
            rendimiento_hortaliza = float(cantidad_hortaliza) / float(area_hortaliza)
        except:
            rendimiento_hortaliza = 0

        #ingresos
        #cafe
        ingreso_cafe = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 1).aggregate(
                            ventas = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['ventas']

        try:
            ingreso_cafe = ingreso_cafe / tipo_cambio[0]
        except:
            pass

        try:
            ha_cafe = (filtro.filter(anio = year,produccion__cultivo__tipo = 1).aggregate(
                                ha = Sum('produccion__area_sembrada'))['ha']) * hectarea
        except:
            ha_cafe = 0

        precio_prom_cafe = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 1).aggregate(
                            precio = Avg('destinoproduccion__mercado__precio'))['precio']

        try:
            precio_prom_cafe = precio_prom_cafe / tipo_cambio[0]
        except:
            pass


        #cacao
        ingreso_cacao = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 2).aggregate(
                            ventas = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['ventas']

        try:
            ingreso_cacao = ingreso_cacao / tipo_cambio[0]
        except:
            pass

        try:
            ha_cacao = (filtro.filter(anio = year,produccion__cultivo__tipo = 2).aggregate(
                                ha = Sum('produccion__area_sembrada'))['ha']) * hectarea
        except:
            ha_cacao = 0

        precio_prom_cacao = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 2).aggregate(
                            precio = Avg('destinoproduccion__mercado__precio'))['precio']

        try:
            precio_prom_cacao = precio_prom_cacao / tipo_cambio[0]
        except:
            pass

        #hortalizas
        ingreso_hortalizas = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 3).aggregate(
                            ventas = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['ventas']

        try:
            ingreso_hortalizas = ingreso_hortalizas / tipo_cambio[0]
        except:
            pass

        try:
            ha_hortalizas = (filtro.filter(anio = year,produccion__cultivo__tipo = 3).aggregate(
                                ha = Sum('produccion__area_sembrada'))['ha']) * hectarea
        except:
            ha_hortalizas = 0

        precio_prom_hortalizas = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 3).aggregate(
                            precio = Avg('destinoproduccion__mercado__precio'))['precio']

        try:
            precio_prom_hortalizas = precio_prom_hortalizas / tipo_cambio[0]
        except:
            pass

        #contribucion al ingreso por rubro

        try:
            ingreso_no_agro = (filtro.filter(anio = year).aggregate(
                        total = Sum(F('fuenteingresos__cantidad_mensual') * F('fuenteingresos__cantidad_veces')))['total']) / tipo_cambio[0]
        except:
            ingreso_no_agro = 0

        try:
            otros_cultivos = (filtro.filter(anio = year).aggregate(total = Sum(
                            'ingresosotroscultivos__ingreso_anual'))['total']) / tipo_cambio[0]
        except:
            otros_cultivos = 0

        try:
            ganaderia = (filtro.filter(anio = year).aggregate(total = Sum(
                    F('ingresosactividadesganaderia__cantidad_mensual') * F('ingresosactividadesganaderia__cantidad_veces')))['total']) / tipo_cambio[0]
        except:
            ganaderia = 0

        otros_ingresos = otros_cultivos + ganaderia

        try:
            cafe = (filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 1).aggregate(total = Sum(
                        F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['total']) / tipo_cambio[0]
        except:
            cafe = 0

        try:
            cacao = (filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 2).aggregate(total = Sum(
                        F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['total']) / tipo_cambio[0]
        except:
            cacao = 0

        try:
            hortalizas = (filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 3).aggregate(total = Sum(
                        F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['total']) / tipo_cambio[0]

        except:
            hortalizas = 0


        #detalle de los cultivos
        ventas_cafe = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 1).aggregate(
                            ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

        ventas_cacao = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 2).aggregate(
                            ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']

        ventas_hortalizas = filtro.filter(anio = year,destinoproduccion__cultivo__tipo = 3).aggregate(
                            ventas = Sum('destinoproduccion__mercado__cantidad'))['ventas']


        anios[year] = (cultivos,ventas,cafe_prod,rendimiento_cafe,area_cafe,sembrada_cafe,
                        cacao_prod,rendimiento_cacao,area_cacao,sembrada_cacao,
                        hortaliza_prod,rendimiento_hortaliza,area_hortaliza,sembrada_hortaliza,
                        ingreso_cafe,ha_cafe,precio_prom_cafe,ingreso_cacao,ha_cacao,precio_prom_cacao,
                        ingreso_hortalizas,ha_hortalizas,precio_prom_hortalizas,
                        ingreso_no_agro,otros_ingresos,cafe,cacao,hortalizas,
                        ventas_cafe,ventas_cacao,ventas_hortalizas)

    return render(request, template, locals())

#ajax
def get_deptos(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []

    foo = Encuesta.objects.filter(productor__pais__in = lista).order_by('productor__pais__nombre').distinct().values_list('productor__pais__id', flat=True)

    deptos = Departamento.objects.filter(pais__id = foo).order_by('nombre').values('id', 'nombre')

    return HttpResponse(simplejson.dumps(list(deptos)), content_type = 'application/json')

def get_munis(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                depto = Departamento.objects.get(id = id)
                municipios = Municipio.objects.filter(departamento__id = depto.id).order_by('nombre')
                lista1 = []
                for municipio in municipios:
                    muni = {}
                    muni['id'] = municipio.id
                    muni['nombre'] = municipio.nombre
                    lista1.append(muni)
                    dicc[depto.nombre] = lista1
            except:
                pass

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type = 'application/json')
