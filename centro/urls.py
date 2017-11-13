# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
from .models import Center

from .views import CenterDetailView, CenterCreateView, CenterUpdateView, CenterListView, PictureAdd, \
                    PollForm, PollResult, CreateKnowledge, UpdateKnowledge

app_name = 'Center'

urlpatterns = [
    url(r'^$', CenterListView.as_view(), name='home'),
    url(r'^gratuitos/$',
        CenterListView.as_view(queryset=Center.objects.filter(free=True), template_name='center_free_list.html'),
        name='home_free'),
    url(r'^destino/ver/(?P<slug>[-\w ]+)/$', CenterDetailView.as_view(), name='center_detail'),
    url(r'^destino/crear/$', CenterCreateView.as_view(), name='center_create'),
    url(r'^destino/editar/$', CenterUpdateView.as_view(), name='center_edit'),
    url(r'^destino/conocimiento/crear/$', CreateKnowledge .as_view(), name='knowledge_create'),
    url(r'^destino/conocimiento/editar/$', UpdateKnowledge .as_view(), name='knowledge_update'),
    url(r'^destino/imagen/agregar/$', PictureAdd.as_view(), name='add_image'),
    url(r'^encuesta/$', PollForm.as_view(), name='encuesta'),
    url(r'^encuesta/(?P<pk>[-\d ]+)/$', PollResult.as_view(), name='encuesta_resultado'),
]
