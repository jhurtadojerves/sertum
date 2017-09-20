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

    def get_context_data(self, **kwargs):
        context = super(CreateServiceView, self).get_context_data(**kwargs)
        context['request'] = self.request
        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user=self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True

        return context

    def get_form(self):
        form = super(CreateServiceView, self).get_form()
        form.fields['service'].widget.attrs.update({'class': 'form-control'})
        return form


class ListServiceView(ListView):
    model = Service
    template_name = "service_list.html"
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super(ListServiceView, self).get_context_data(**kwargs)
        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user=self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True

        return context


class ListServiceViewFilter(ListView):
    model = Center
    template_name = "center_list_by_service.html"
    context_object_name = "centers"

    def get_context_data(self, **kwargs):
        context = super(ListServiceViewFilter, self).get_context_data(**kwargs)
        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user=self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True

        return context

    def get_queryset(self):
        qs = super(ListServiceViewFilter, self).get_queryset()
        return qs.filter(service__slug=self.kwargs['slug']).distinct()
