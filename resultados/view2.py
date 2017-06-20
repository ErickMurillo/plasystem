from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from organizaciones.models import *
from django.db.models import Sum, Count, Avg, F

from .views import _queryset_filtrado

def grafo_comparativo(request, template='resultados/grafo-resultado.html'):
	filtro = _queryset_filtrado(request)[0]
	print filtro

	return render(request, template, {})