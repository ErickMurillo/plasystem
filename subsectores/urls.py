from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ver/informe-planes-anuales/$', views.list_informe, name='lista-informe'),
    url(r'^ver/plan/(?P<pk>\d+)/$', views.ver_informe, name='ver-informe'),

]