# -*- encoding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve



from .views import CenterDetailView, CenterCreateView, CenterUpdateView, CenterListView

app_name = 'Center'

urlpatterns = [
    url(r'^$', CenterListView.as_view(), name='home'),
    url(r'^centro/ver/(?P<slug>[-\w ]+)/$', CenterDetailView.as_view(), name='center_detail'),
    url(r'^centro/crear/$', CenterCreateView.as_view(), name='center_create'),
    url(r'^centro/editar/(?P<slug>[-\w ]+)/$', CenterUpdateView .as_view(), name='center_edit'),


    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),


    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }, name = 'ver_imagen'),
]