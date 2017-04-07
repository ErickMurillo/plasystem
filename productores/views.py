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
        conservacion_suelo = ((filtro.filter(anio = year).aggregate(total = Avg(F('conservacionsuelo__erosion')
                                + F('conservacionsuelo__sanilizacion')
                                + F('conservacionsuelo__contaminacion_suelo')
                                + F('conservacionsuelo__materia_organica')))['total']) / 12) * 100
                                
        anios[year] = (cafe,cacao,hortalizas,conservacion_suelo)

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
