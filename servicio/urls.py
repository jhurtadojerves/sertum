# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin

from .views import CreateServiceView, ListServiceView, ListServiceViewFilter
from .models import Service


app_name = 'Service'

urlpatterns = [
    url(r'^servicios/$', ListServiceView.as_view(), name='service_list'),
    url(r'^servicios/crear/$', CreateServiceView.as_view(), name='service_create'),
    url(r'^servicios/(?P<slug>[-\w ]+)/$', ListServiceViewFilter.as_view(), name='center_service_list'),
]