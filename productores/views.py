from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def _queryset_filtrado(request):
    params = {}

    if request.session['anio']:
        params['anio__in'] = request.session['anio']

    if request.session['pais']:
        params['productor__pais__in'] = request.session['pais']

    if request.session['departamento']:
        params['productor__departamento__in'] = request.session['departamento']

    if request.session['municipio']:
        params['productor__municipio__in'] = request.session['municipio']

    if request.session['organizacion']:
        params['productor__organizacion__in'] = request.session['organizacion']

    if request.session['sexo']:
        params['productor__sexo'] = request.session['sexo']

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
            # request.session['edad'] = form.cleaned_data['edad']

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
            # del request.session['edad']
        except:
            pass

    return render(request, template, locals())

@login_required
def dashboard_productores(request,template="productores/dashboard.html"):
    return render(request, template, locals())
