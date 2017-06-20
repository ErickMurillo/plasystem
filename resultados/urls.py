from django.conf.urls import url
from django.contrib import admin
from .views import *
from .view2 import *

urlpatterns = [
    url(r'^$', consulta, name='consulta-org'),
    url(r'^dashboard/$', dashboard, name='dashboard-org'),
    url(r'^grafo/resultado/$', grafo_comparativo, name='grafo-comparativo'),
]