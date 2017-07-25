from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView, ListView, FormView, View

from .models import Center, Picture, Knowledge, Poll
from usuario.models import User as Usuario
from .form import CenterCreateForm, PictureCreateForm, PictureAddForm, KnowledgePollForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required

from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import PermissionRequiredMixin

import operator

# Create your views here.

class CenterDetailView(DetailView):
    model = Center
    template_name = 'center_detail.html'
    slug_field = 'slug'
    context_object_name = 'center'

    def get_context_data(self, **kwargs):
        context =  super(CenterDetailView, self).get_context_data(**kwargs)
        context['pictures'] = Picture.objects.filter(center__slug=self.object.slug)

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
    permission_required = "usuario.add_center"
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

class PollForm(CreateView):
    template_name = "poll_form.html"
    form_class = KnowledgePollForm
    success_url = reverse_lazy('Center:encuesta_resultado')


    def get_context_data(self, **kwargs):
        context = super(PollForm, self).get_context_data(**kwargs)
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)

        poll = form.save()



        return HttpResponseRedirect(str(poll.id))

class PollResult(DetailView):
    model = Poll
    template_name="poll_result.html"
    context_object_name = 'poll'
    def get_context_data(self, **kwargs):
        context = super(PollResult, self).get_context_data(**kwargs)
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



        #poll = Poll.objects.filter(id=self.kwargs['pk'])
        poll = self.get_object()

        money_int = int(poll.money_per_person)

        polls = Knowledge.objects.filter(group_type=poll.group_type, activities=poll.activities,
                                         money_per_person__in=range(0, money_int))
        # money_per_person__range=range(0, money_int),



        pfilter = list()

        if polls.exists():
            for p in polls:
                contador = 3
                if p.transport == poll.transport:
                    contador = contador + 1
                if p.food == poll.food:
                    contador = contador + 1
                if p.extreme_sport == poll.extreme_sport:
                    contador = contador + 1
                if p.sport_fishing == poll.sport_fishing:
                    contador = contador + 1
                if p.night_bar == poll.night_bar:
                    contador = contador + 1
                if p.has_lodging == poll.has_lodging:
                    contador = contador + 1
                pfilter.append((p.center, contador))
            pFilterOrder = pfilter.sort(key=lambda x: x[1])

            centerAndValue = pfilter.pop(0)

        else:
            centerAndValue = ("No se ha encontrado ningún centro que cumpla con sus especificaciones", "")

        context['centerS'] = centerAndValue[0]
        context['pictures'] = Picture.objects.filter(center__slug=centerAndValue[0].slug)
        context['valueS'] = centerAndValue[1]

        return context
