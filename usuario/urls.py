# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin




from .views import RegisterUserCreateView

app_name = 'User'

urlpatterns = [
    url(r'^usuario/registrar/$', RegisterUserCreateView.as_view(), name='registrar'),

]