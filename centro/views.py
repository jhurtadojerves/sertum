from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .models import Center
from usuario.models import User as Usuario
from .form import CenterCreateForm, ServiceFormset
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class CenterDetailView(DetailView):
    model = Center
    template_name = 'center_detail.html'
    slug_field = 'slug'
    context_object_name = 'center'

class CenterCreateView(CreateView):
    model = Center
    template_name = 'center_create.html'
    form_class = CenterCreateForm
    context_object_name = 'center'

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(id = request.user.id)
        self.model.user = usuario

        temp = self.form_class(request.POST).save()
        return HttpResponseRedirect(reverse('Center:center_detail', args=[str(temp.slug)]))





class CenterUpdateView(UpdateView):
    model = Center
    template_name = 'center_edit.html'
    slug_field = 'slug'
    form_class = CenterCreateForm
    context_object_name = 'center'

class CenterListView(ListView):
    model = Center
    template_name = 'center_list.html'
    context_object_name = 'centers'