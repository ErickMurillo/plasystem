from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import json as simplejson
from django.db.models import Sum, Count, Avg, F
import collections

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

@login_required
def dashboard_productores_filtrado(request,template="productores/dashboard.html"):
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
    #     try:
    #         del request.session['anio']
    #         del request.session['pais']
    #         del request.session['departamento']
    #         del request.session['municipio']
    #         del request.session['organizacion']
    #         del request.session['sexo']
    #         del request.session['edad']
    #     except:
    #         pass

    filtro = _queryset_filtrado(request)

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
    years = request.session['anio']
    anios = collections.OrderedDict()
    for year in years:
        #ingresos
        cafe = filtro.filter(destinoproduccion__cultivo__tipo = 1, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        cacao = filtro.filter(destinoproduccion__cultivo__tipo = 2, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        hortalizas = filtro.filter(destinoproduccion__cultivo__tipo = 3, anio = year).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

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

        # grafica Aumento del indice de manejo de plaga
        encuestas = filtro.count()
        cultivos = {}
        for obj in CULTIVOS_MIP:
            total_material = 0
            for x in MATERIAL_CHOICES:
                material_siembra_sano = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__material_siembra_sano__icontains = x[0]).count()
                total_material = total_material + material_siembra_sano
            total_material = (total_material / float(encuestas)) * 33.33

            total_preparacion = 0
            for x in PREPARACION_TERRENO:
                preparacion_terreno = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__preparacion_terreno__icontains = x[0]).count()
                total_preparacion = total_preparacion + preparacion_terreno
            total_preparacion = (total_preparacion / float(encuestas)) * 20

            total_control = 0
            for x in CONTROL_MALEZAS:
                control_malezas = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__control_malezas__icontains = x[0]).count()
                total_control = total_control + control_malezas
            total_control = (total_control / float(encuestas)) * 50

            total_fertilizacion = 0
            for x in FERTILIZACION_ADECUADA:
                fertilizacion_adecuada = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__fertilizacion_adecuada__icontains = x[0]).count()
                total_fertilizacion = total_fertilizacion + fertilizacion_adecuada
            total_fertilizacion = (total_fertilizacion / float(encuestas)) * 33.33

            total_densidad = 0
            for x in DENSIDAD_SOMBRA:
                densidad_siembra = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__densidad_siembra__icontains = x[0]).count()
                total_densidad = total_densidad + densidad_siembra
            total_densidad = (total_densidad / float(encuestas)) * 50

            total_plagas = 0
            for x in DENSIDAD_SOMBRA:
                control_plagas_enfermedades = filtro.filter(anio = year,practicasmip__cultivo = obj[0],practicasmip__control_plagas_enfermedades__icontains = x[0]).count()
                total_plagas = total_plagas + control_plagas_enfermedades
            total_plagas = (total_plagas / float(encuestas)) * 50

            cultivos[obj[0]] = (total_material,total_preparacion,total_control,
                                total_fertilizacion,total_densidad,total_plagas)

        anios[year] = (cafe,cacao,hortalizas,conservacion_suelo,uso_eficiente_agua,gestion_recursos_naturales,
                        cambio_climatico,biodiversidad,paisaje_sostenible,cultivos)
    print anios


    #indice total produccion sustentable -------------------------------------------------
    last_year = years[-1]
    #conservacion suelo
    try:
        conservacion_suelo = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('conservacionsuelo__erosion')
                                + F('conservacionsuelo__sanilizacion')
                                + F('conservacionsuelo__contaminacion_suelo')
                                + F('conservacionsuelo__materia_organica')))['total']) / 12) * 100
    except:
        conservacion_suelo = 0

    #uso_eficiente_agua
    try:
        uso_eficiente_agua = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('usoeficienteagua__gestion_riesgo')
                                + F('usoeficienteagua__retencion_agua')
                                + F('usoeficienteagua__eficiencia_agua')
                                + F('usoeficienteagua__contaminacion_agua')))['total']) / 12) * 100
    except:
        uso_eficiente_agua = 0

    #gestion_recursos_naturales
    try:
        gestion_recursos_naturales = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('gestionrecursosnaturales__pruebas_suelo')
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
        cambio_climatico = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('cambioclimatico__emision_carbono')
                                + F('cambioclimatico__procesamiento_transporte')))['total']) / 6) * 100
    except:
        cambio_climatico = 0

    #biodiversidad
    try:
        biodiversidad = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('biodiversidad__diversidad_vegetal')
                                + F('biodiversidad__diversidad_genetica')
                                + F('biodiversidad__uso_tierra')))['total']) / 9) * 100
    except:
        biodiversidad = 0

    #paisaje_sostenible
    try:
        paisaje_sostenible = ((filtro.filter(anio = last_year).aggregate(total = Avg(F('paisajsostenible__salvaguardar_ecosistemas')
                                + F('paisajesostenible__proteccion_vida_silvestre')
                                + F('paisajesostenible__tierras_agricolas')
                                + F('paisajesostenible__especies_invasoras')))['total']) / 12) * 100
    except:
        paisaje_sostenible = 0

    indice = (conservacion_suelo + uso_eficiente_agua + gestion_recursos_naturales
                + cambio_climatico + paisaje_sostenible) / 5

    return render(request, template, locals())

@login_required
def dashboard_productores_nicaragua(request,template="productores/dashboard.html"):
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

    filtro = Encuesta.objects.filter(productor__pais__nombre = 'Nicaragua')

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
    years = fecha_choice()
    anios = collections.OrderedDict()
    for year in years:
        #ingresos
        cafe = filtro.filter(destinoproduccion__cultivo__tipo = 1, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        cacao = filtro.filter(destinoproduccion__cultivo__tipo = 2, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        hortalizas = filtro.filter(destinoproduccion__cultivo__tipo = 3, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        #
        anios[year[0]] = (cafe,cacao,hortalizas)

    return render(request, template, locals())

@login_required
def dashboard_productores_honduras(request,template="productores/dashboard.html"):
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

    filtro = Encuesta.objects.filter(productor__pais__nombre = 'Honduras')

    hectarea = 0.7050

    #conteos generales
    familias = filtro.distinct().count()
    hombres = filtro.filter(productor__sexo = 'Hombre').count()
    mujeres = filtro.filter(productor__sexo = 'Mujer').count()
    menores_35 = filtro.filter(productor__edad = 1).count()
    manzanas = filtro.aggregate(total = Avg('areafinca__area'))['total']
    hectareas = manzanas * hectarea
    certificacion = filtro.filter(certificacion__certificacion = 'Si').count()

    #graficas
    years = fecha_choice()
    anios = collections.OrderedDict()
    for year in years:
        #ingresos
        cafe = filtro.filter(destinoproduccion__cultivo__tipo = 1, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        cacao = filtro.filter(destinoproduccion__cultivo__tipo = 2, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        hortalizas = filtro.filter(destinoproduccion__cultivo__tipo = 3, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        #
        anios[year[0]] = (cafe,cacao,hortalizas)

    return render(request, template, locals())

@login_required
def dashboard_productores_guatemala(request,template="productores/dashboard.html"):
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

    filtro = Encuesta.objects.filter(productor__pais__nombre = 'Guatemala')

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
    years = fecha_choice()
    anios = collections.OrderedDict()
    for year in years:
        #ingresos
        cafe = filtro.filter(destinoproduccion__cultivo__tipo = 1, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        cacao = filtro.filter(destinoproduccion__cultivo__tipo = 2, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        hortalizas = filtro.filter(destinoproduccion__cultivo__tipo = 3, anio = year[0]).aggregate(
                sum = Sum(F('destinoproduccion__mercado__cantidad') * F('destinoproduccion__mercado__precio')))['sum']

        #
        anios[year[0]] = (cafe,cacao,hortalizas)

    return render(request, template, locals())

#ajax
def get_deptos(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []

    foo = Encuesta.objects.filter(productor__pais__in = lista).order_by('productor__pais__nombre').distinct().values_list('productor__pais__id', flat=True)
    print foo
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
