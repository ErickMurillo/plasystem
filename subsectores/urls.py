from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.consulta_proyectos, name='index-subsectores'),
    url(r'^ver/informe-planes-anuales/$', views.list_informe, name='lista-informe'),
    url(r'^subsector/ver/proyecto/(?P<pk>\d+)/$', views.ver_informe, name='subsector-ver-proyecto'),

]