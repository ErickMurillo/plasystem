from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', consulta_productores, name='index-productores'),
    url(r'^dashboard/$', dashboard_productores, name='dashboard-productores'),

    #ajax
    url(r'^ajax/deptos/$', get_deptos, name='get-deptos'),
    url(r'^ajax/municipios/$', get_munis, name='get-munis'),
]
