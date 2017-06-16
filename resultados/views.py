from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from organizaciones.models import *
from django.db.models import Sum, Count, Avg, F
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

    miembros_hombres = ProductoresProveedores.objects.filter(organizacion__in = filtro[0].values_list(
                        'organizacion',flat=True)).aggregate(total = Sum('activos_hombre'))['total']

    miembros_mujeres = ProductoresProveedores.objects.filter(organizacion__in = filtro[0].values_list(
                        'organizacion',flat=True)).aggregate(total = Sum('activos_mujer'))['total']
    
    return render(request, template, locals())