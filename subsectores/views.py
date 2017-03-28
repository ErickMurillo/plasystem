from django.shortcuts import render, get_object_or_404
from .models import Componentes, RegistroPlanAnual, CHOICES_MESES
# Create your views here.


def list_informe(request, template='admin/lista_informe_plan_anual.html'):
	plan_anual = Componentes.objects.all()
	return render(request, template, locals())

def ver_informe(request, template='admin/ver_informe.html', pk=None):
	componente = get_object_or_404(Componentes, id=pk)
	meses = CHOICES_MESES
	informe = RegistroPlanAnual.objects.filter(proyecto__componente__id=pk)
	return render(request, template, locals())