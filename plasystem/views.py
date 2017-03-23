from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def index(request,template="index.html"):
    return render(request, template, locals())
