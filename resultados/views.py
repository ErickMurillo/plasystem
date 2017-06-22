from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from organizaciones.models import *
from django.db.models import Sum, Count, Avg, F
import json as simplejson
import collections

# Create your views here.

def _queryset_filtrado(request):
    params = {}

    if request.session['anio']:
        params['year__in'] = request.session['anio']

    if request.session['organizacion']:
        params['organizacion__in'] = request.session['organizacion']

    if request.session['pais']:
        params['pais'] = request.session['pais']


	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	a = ResultadosEvaluacion.objects.filter(**params)
	b = ResultadosImplementacion.objects.filter(**params)
    return a,b

@login_required
def consulta(request,template="organizaciones/consulta.html"):
    if request.method == 'POST':
        mensaje = None
        form = OrganizacionesForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['pais'] = form.cleaned_data['pais']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

            return HttpResponseRedirect('/organizaciones/dashboard/')

        else:
            centinela = 0

    else:
        form = OrganizacionesForm()
        mensaje = "Existen alguno errores"
        try:
            del request.session['anio']
            del request.session['organizacion']
            del request.session['pais']
        except:
            pass

    return render(request, template, locals())

@login_required
def dashboard(request,template="organizaciones/dashboard.html"):
    if request.method == 'POST':
        mensaje = None
        form = OrganizacionesForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['pais'] = form.cleaned_data['pais']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

        else:
            centinela = 0

    else:
        form = OrganizacionesForm()
        mensaje = "Existen alguno errores"

    filtro = _queryset_filtrado(request)

    # unificar organizaciones de los dos modelos
    list_ev_org = []
    for x in filtro[0].values_list('organizacion',flat=True):
        list_ev_org.append(x)

    list_im_org = []
    for x in filtro[1].values_list('organizacion',flat=True):
        list_im_org.append(x)

    result_list = list(sorted(set(list_ev_org + list_im_org)))

    # --------
    orgs = Organizacion.objects.filter(id__in = result_list)

    total_hombres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('total_hombre'))['total']
    total_mujeres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('total_mujer'))['total']
    

    activos_hombres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('activos_hombre'))['total']
    activos_mujeres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('activos_mujer'))['total']
    
    jovenes_hombres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('jovenes_hombre'))['total']
    jovenes_mujeres = ProductoresProveedores.objects.filter(organizacion__in = result_list).aggregate(total = Sum('jovenes_mujer'))['total']
    

    # empleados de la org tiempo completo, preg 22
    empleados_org = EmpleadosOrganizacion.objects.filter(organizacion__in = result_list,opcion = 1).aggregate(
                                            total_hombre = Sum('total_hombre'),
                                            total_mujer = Sum('total_mujer'),
                                            adultos_hombre = Sum('adultos_hombre'),
                                            adultos_mujer = Sum('adultos_mujer'),
                                            jovenes_hombre = Sum('jovenes_hombre'),
                                            jovenes_mujer = Sum('jovenes_mujer'))

    # servicios y productos
    sectores = {}
    for obj in CHOICE_SECTOR:
        conteo = SectoresProductos.objects.filter(organizacion__in = result_list, sector = obj[0]).count()

        productos = []
        for x in Productos.objects.filter(sector__sector = obj[0]):
            prod = ProductosOrg.objects.filter(id = x.producto1.id)
            productos.append((prod,prod.count()))

        sectores[obj[1]] = conteo,productos


    # situacion legal y organizativa de org
    personeria = Organizacion.objects.filter(id__in = result_list,personeria = 1).count()
    en_operaciones = Organizacion.objects.filter(id__in = result_list,en_operaciones = 1).count()
    apoyo = Organizacion.objects.filter(id__in = result_list,apoyo = 1).count()

    return render(request, template, locals())

def detail_org(request,template='organizaciones/detalle-org.html', id=None):
    if request.method == 'POST':
        mensaje = None
        form = OrganizacionesForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['pais'] = form.cleaned_data['pais']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1

            return HttpResponseRedirect('/organizaciones/dashboard/')

        else:
            centinela = 0

    else:
        form = OrganizacionesForm()
        mensaje = "Existen alguno errores"

    org = Organizacion.objects.get(id = id)

    # cooperativas miembros
    cooprativas = NumeroCooperativa.objects.filter(organizacion_id = id).values_list('numero_cooperativa', flat=True)

    # areas que reciben apoyo
    areas = {}
    for obj in Areas.objects.all():
        x = ApoyoDonante.objects.filter(areas = obj, organizacion__id = id).count()
        areas[obj] = x

    # miembros
    miembros = {}
    for obj in CHOICE_MIEMBROS:
        result = MiembrosOficiales.objects.filter(organizacion__id = id,opcion = obj[0]).aggregate(
                                        total_h = Sum('total_hombre'),
                                        total_m = Sum('total_mujer'),
                                        activos_h = Sum('activos_hombre'),
                                        activos_m = Sum('activos_mujer'),
                                        jovenes_h = Sum('jovenes_hombre'),
                                        jovenes_m = Sum('jovenes_mujer'))

        miembros[obj[1]] = result['total_h'],result['total_m'],result['activos_h'],result['activos_m'],result['jovenes_h'],result['jovenes_m']

    # productores proveedores
    productores = []
    for obj in CHOICE_PROVEEDORES:
        result = ProductoresProveedores.objects.filter(organizacion__id = id,opcion = obj[0]).aggregate(
                                        total_h = Sum('total_hombre'),
                                        total_m = Sum('total_mujer'),
                                        activos_h = Sum('activos_hombre'),
                                        activos_m = Sum('activos_mujer'),
                                        jovenes_h = Sum('jovenes_hombre'),
                                        jovenes_m = Sum('jovenes_mujer'))

        productores.append((result['total_h'],result['total_m'],result['activos_h'],result['activos_m'],result['jovenes_h'],result['jovenes_m']))


    # tipo de orgs a las que pertence
    org_pertenece = OrganizacionPertenece.objects.filter(organizacion__id = id).values_list('organizaciones__nombre',flat=True)

    # empleados de la org
    empleados = {}
    for obj in CHOICE_EMPLEADOS:
        result = EmpleadosOrganizacion.objects.filter(organizacion__id = id,opcion = obj[0]).aggregate(
                                        total_h = Sum('total_hombre'),
                                        total_m = Sum('total_mujer'),
                                        adultos_h = Sum('adultos_hombre'),
                                        adultos_m = Sum('adultos_mujer'),
                                        jovenes_h = Sum('jovenes_hombre'),
                                        jovenes_m = Sum('jovenes_mujer'))

        empleados[obj[1]] = result['total_h'],result['total_m'],result['adultos_h'],result['adultos_m'],result['jovenes_h'],result['jovenes_m']

    # scope pro
    years = request.session['anio']
    dic_anios = collections.OrderedDict()
    for year in years:
        gestion_interna = GestionInterna.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        operaciones = Operaciones.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        sostenibilidad = Sostenibilidad.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        gestion_financiera = GestionFinanciera.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        desempeno_financiero = DesempenoFinanciero.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        suministros = Suministros.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        mercados = Mercados.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        riesgo_externos = RiesgoExternos.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)
        facilitadores = Facilitadores.objects.filter(opciones = 1,resultado__year = year, resultado__organizacion__id = id).values_list('valor',flat=True)

        dic_anios[year] = gestion_interna, operaciones, sostenibilidad, gestion_financiera, desempeno_financiero, suministros, mercados, riesgo_externos, facilitadores

    return render(request, template, locals())

#ajax
def get_org(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    results = []

    foo = Pais.objects.filter(id__in = lista).order_by('nombre').distinct().values_list('id', flat=True)
    orgs = Organizacion.objects.filter(pais__id__in=foo).order_by('nombre').values('id', 'nombre')

    return HttpResponse(simplejson.dumps(list(orgs)), content_type = 'application/json')