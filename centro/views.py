from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .models import Center, Picture
from usuario.models import User as Usuario
from .form import CenterCreateForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


# Create your views here.

class CenterDetailView(DetailView):
    model = Center
    template_name = 'center_detail.html'
    slug_field = 'slug'
    context_object_name = 'center'

    def get_context_data(self, **kwargs):
        context =  super(CenterDetailView, self).get_context_data(**kwargs)
        context['pictures'] = Picture.objects.filter(center__slug = self.object.slug)
        return context

class CenterCreateView(CreateView):
    model = Center
    template_name = 'center_create.html'
    form_class = CenterCreateForm
    context_object_name = 'center'

    @method_decorator(permission_required('usuario.add_center'))
    def dispatch(self, *args, **kwargs):
        return super(CenterCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CenterCreateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        user = Usuario.objects.get(user = self.request.user)
        center = Center.objects.filter(user=user)
        if center.exists():
            context['verification'] = False
            context['center'] = Center.objects.get(user=user)
        else:
            context['verification'] = True

        return context


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