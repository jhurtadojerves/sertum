# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin




from .views import RegisterUserCreateView, ValidationUserListView, AddPermissionUpdateView

app_name = 'User'

urlpatterns = [
    url(r'^usuario/registrar/$', RegisterUserCreateView.as_view(), name='registrar'),
    url(r'^usuario/validar/$', ValidationUserListView.as_view(), name='listar_sin_permisos'),
    url(r'^usuario/validar/(?P<pk>[-\w ]+)/$', AddPermissionUpdateView.as_view(), name='add_permission'),
]