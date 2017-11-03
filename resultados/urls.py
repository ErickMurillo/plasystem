from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', consulta, name='consulta-org'),
    url(r'^dashboard/ficha-organizacion/(?P<id>\d+)/$', detail_org, name='detail-org'),
    url(r'^dashboard/$', dashboard, name='dashboard-org'),
    url(r'^ajax/orgs/$', get_org, name='get-org'),
    

    url(r'^ver/organizaciones/$', lista_organizacion, name='lista-organizacion'),
    url(r'^ver/organizacion/(?P<pk>\d+)/$', detalle_organizacion, name='lista-organizacion'),
]