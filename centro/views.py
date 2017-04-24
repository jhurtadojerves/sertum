from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView, ListView, FormView

from .models import Center, Picture
from usuario.models import User as Usuario
from .form import CenterCreateForm, PictureCreateForm, PictureAddForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.

class CenterDetailView(DetailView):
    model = Center
    template_name = 'center_detail.html'
    slug_field = 'slug'
    context_object_name = 'center'

    def get_context_data(self, **kwargs):
        context =  super(CenterDetailView, self).get_context_data(**kwargs)
        context['pictures'] = Picture.objects.filter(center__slug = self.object.slug)

        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user = self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True


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
        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user = self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
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

    def get_context_data(self, **kwargs):
        context = super(CenterListView, self).get_context_data(**kwargs)
        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user = self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True

        return context

class PictureAdd(PermissionRequiredMixin, FormView):
    permission_required = "is_authenticated"
    template_name = "add_picture.html"
    form_class = PictureAddForm

    def form_valid(self, form):
        picture = self.get_form_kwargs().get('files')['picture']

        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user=self.request.user)
            center = Center.objects.filter(user=user)

            if center.exists():
                center = Center.objects.get(user=user)
                picture_object = Picture(picture=picture, center=center)
                picture_object.save()
                return HttpResponseRedirect(reverse_lazy('Center:center_detail', kwargs={'slug': center.slug}))
                #return HttpResponseRedirect(reverse_lazy('Center:home'))

    def get_context_data(self, **kwargs):
        context = super(PictureAdd, self).get_context_data(**kwargs)
        context['request'] = self.request
        if self.request.user.is_authenticated():
            user = Usuario.objects.filter(user = self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = True
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = False
        else:
            context['verification'] = True

        return context