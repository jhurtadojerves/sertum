# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin



from .views import CenterDetailView

app_name = 'Center'

urlpatterns = [
    url(r'^centro/(?P<slug>[-\w ]+)/$', CenterDetailView.as_view(), name='center_detail'),

]