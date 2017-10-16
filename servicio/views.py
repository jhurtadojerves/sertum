from django.shortcuts import render

from django.views.generic import CreateView, ListView, TemplateView

from .models import Service
from usuario.models import User as Usuario
from centro.models import Center, ServiceCenter

from django.urls import reverse, reverse_lazy

# Create your views here.


class CreateServiceView(CreateView):
    model = ServiceCenter
    template_name = "service_create.html"
    context_object_name = "service"
    fields = ['service', 'center', 'cost', 'observation', ]
    success_url = "/"

    def get_form(self):
        form = super(CreateServiceView, self).get_form()
        form.fields['service'].widget.attrs.update({'class': 'form-control'})
        return form


class ListServiceView(ListView):
    model = Service
    template_name = "service_list.html"
    context_object_name = 'services'


class ListServiceViewFilter(ListView):
    model = Center
    template_name = "center_list_by_service.html"
    context_object_name = "centers"

    def get_queryset(self):
        qs = super(ListServiceViewFilter, self).get_queryset()
        return qs.filter(service__slug=self.kwargs['slug']).distinct()
