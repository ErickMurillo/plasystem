from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', consulta_productores, name='index-productores'),
    url(r'^dashboard/$', dashboard_productores_filtrado, name='dashboard-productores'),
    url(r'^dashboard/nicaragua$', dashboard_productores_nicaragua, name='dashboard-productores-nicaragua'),
    url(r'^dashboard/honduras$', dashboard_productores_honduras, name='dashboard-productores-honduras'),
    url(r'^dashboard/guatemala$', dashboard_productores_guatemala, name='dashboard-productores-guatemala'),
    #ajax
    url(r'^ajax/deptos/$', get_deptos, name='get-deptos'),
    url(r'^ajax/municipios/$', get_munis, name='get-munis'),
]
