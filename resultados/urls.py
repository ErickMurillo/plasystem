from django.conf.urls import url
from django.contrib import admin
from .views import *
from .view2 import *

urlpatterns = [
    url(r'^$', consulta, name='consulta-org'),
    url(r'^dashboard/$', dashboard, name='dashboard-org'),
    url(r'^ajax/orgs/$', get_org, name='get-org'),
    url(r'^dashboard/ficha-organizacion/(?P<id>[0-9])/$', detail_org, name='detail-org'),

	url(r'^grafo/resultado/$', grafo_comparativo, name='grafo-comparativo'),
]