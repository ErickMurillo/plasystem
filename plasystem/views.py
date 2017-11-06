from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productores.models import *
from reportes.models import *
import json as simplejson
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request,template="index.html"):
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
def list_reportes(request,template="reportes.html"):
    object_list = Reporte.objects.all().order_by('fecha_elaborado')
    
    return render(request, template, locals())

#obtener puntos en el mapa
def obtener_lista(request):
    if request.is_ajax():
        lista = []
        for objeto in Productor.objects.all():
            dicc = dict(nombre=objeto.municipio.nombre, id=objeto.id,
                        lon=float(objeto.municipio.longitud),
                        lat=float(objeto.municipio.latitud)
                        )
            lista.append(dicc)

        serializado = simplejson.dumps(lista)
        return HttpResponse(serializado, content_type = 'application/json')

def obtener_lista_org(request):
    if request.is_ajax():
        lista = []
        for objeto in Organizacion.objects.filter(municipio__isnull = False):
            dicc = dict(nombre=objeto.municipio.nombre, id=objeto.id,
                        lon=float(objeto.municipio.longitud),
                        lat=float(objeto.municipio.latitud)
                        )
            lista.append(dicc)

        serializado = simplejson.dumps(lista)
        return HttpResponse(serializado, content_type = 'application/json')