from django.shortcuts import render, get_object_or_404
from .models import RegistroPlanAnual
# Create your views here.


def list_informe(request, template='admin/lista_informe_plan_anual.html'):
	plan_anual = RegistroPlanAnual.objects.all()
	return render(request, template, locals())

def ver_informe(request, template='admin/ver_informe.html', pk=None):
	informe = get_object_or_404(RegistroPlanAnual, id=pk)
	return render(request, template, locals())