# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin




from .views import CenterDetailView, CenterCreateView, CenterUpdateView, CenterListView, PictureAdd

app_name = 'Center'

urlpatterns = [
    url(r'^$', CenterListView.as_view(), name='home'),
    url(r'^destino/ver/(?P<slug>[-\w ]+)/$', CenterDetailView.as_view(), name='center_detail'),
    url(r'^destino/crear/$', CenterCreateView.as_view(), name='center_create'),
    url(r'^destino/editar/(?P<slug>[-\w ]+)/$', CenterUpdateView .as_view(), name='center_edit'),
    url(r'^imagen/agregar/$', PictureAdd.as_view(), name='add_image'),
]