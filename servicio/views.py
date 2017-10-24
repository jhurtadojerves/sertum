from django.shortcuts import render

from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .models import Service
from usuario.models import User as Usuario
from centro.models import Center, ServiceCenter

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


class CreateServiceView(PermissionRequiredMixin, CreateView):
    permission_required = "usuario.add_center"
    model = ServiceCenter
    template_name = "service_create.html"
    context_object_name = "service"
    fields = ['service', 'cost', 'observation', ]

    def get_form(self):
        form = super(CreateServiceView, self).get_form()
        form.fields['service'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        form.instance.center = self.request.user.profile.center
        form.save()
        return super(CreateServiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Center:center_detail', args=[self.request.user.profile.center.slug])


class EditServiceView(UpdateView):
    permission_required = "usuario.add_center"
    model = ServiceCenter
    template_name = "service_edit.html"
    context_object_name = "service"
    fields = ['cost', 'observation', ]
    slug_field = 'pk'

    def get_success_url(self):
        return reverse("Center:center_detail", args=[self.request.user.profile.center.slug])


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
