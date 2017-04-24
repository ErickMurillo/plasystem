from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
