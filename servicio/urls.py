# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin

from .views import CreateServiceView

app_name = 'Service'

urlpatterns = [
    url(r'^centro/(?P<slug>[-\w ]+)/servicio/crear/$', CreateServiceView.as_view(), name='service_create'),
]