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

from django.shortcuts import get_object_or_404

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


class PollForm(FormView):
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

    def form_valid(self, form):
        form_groups = set(form.cleaned_data.get('group_type').values_list('name'))
        form_activities = set(form.cleaned_data.get('activity').values_list('name'))
        form_transport = set(form.cleaned_data.get('transport').values_list('name'))
        form_food = set(form.cleaned_data.get('food').values_list('name'))

        form_money_per_person = form.cleaned_data.get('money_per_people')
        form_extreme_sport = form.cleaned_data.get('extreme_sport')
        form_sport_fishing = form.cleaned_data.get('sport_fishing')
        form_night_bar = form.cleaned_data.get('night_bar')
        form_has_lodging = form.cleaned_data.get('has_lodging')

        centers = Knowledge.objects.all()
        #centers = Knowledge.objects.filter(id=16)
        centervalue = list()
        for c in centers:
            value = 0
            center = c.center

            groups = set(c.group_type.all().values_list('name'))
            activities = set(c.activities.all().values_list('name'))
            transport = set(c.transport.all().values_list('name'))
            food = set(c.food.all().values_list('name'))

            money_per_person = c.money_per_person
            extreme_sport = c.extreme_sport
            sport_fishing = c.sport_fishing
            night_bar = c.night_bar
            has_lodging = c.has_lodging

            temp_g = groups & form_groups
            value += len(temp_g)

            temp_a = activities & form_activities
            value += len(temp_a)

            temp_t = transport & form_transport
            value += len(temp_t)

            temp_f = food & form_food
            value += len(temp_f)

            if money_per_person <= form_money_per_person:
                value += 1

            if extreme_sport and form_extreme_sport:
                value += 1

            if sport_fishing and form_sport_fishing:
                value += 1

            if night_bar and form_night_bar:
                value += 1

            if has_lodging and form_has_lodging:
                value += 1

            centervalue.append((center, value))

        centervalue.sort(key=lambda x: x[1])

        selectedcenter = centervalue.pop()

        poll = Poll()
        poll.center = selectedcenter[0]
        poll.value = selectedcenter[1]

        poll.user = Usuario.objects.get(user=self.request.user)
        poll.save()
        return HttpResponseRedirect(reverse('Center:encuesta_resultado', args=[poll.id]))


    '''
    def post(self, request, *args, **kwargs):

        form = self.form_class(self.request.POST or None)


        centers = Knowledge.objects.all()
        lista = list()
        for c in centers:
            value = 0
            center = c.center
            groups = c.group_type.all().values_list('name')
            money_per_person = c.money_per_person
            activities = c.activities.all().values_list('name')
            transport = c.transport.all().values_list('name')
            food = c.food.all().values_list('name')
            extreme_sport = c.extreme_sport
            sport_fishing = c.sport_fishing
            night_bar = c.night_bar
            has_lodging = c.has_lodging

            #form_groups = form.group_type
            form_money_per_person = self.request.POST.money_per_people
            form_activities = form.cleaned_data.get('activity').keys()
            form_transport = form.cleaned_data.get('transport').keys()
            form_food = form.cleaned_data.get('food').keys()
            form_extreme_sport = form.extreme_sport
            form_sport_fishing = form.sport_fishing
            form_night_bar = form.night_bar
            form_has_lodging = form.has_lodging


        #return HttpResponseRedirect(str(1))
'''


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

        context['existe'] = True
        context['pictures'] = Picture.objects.filter(center__slug=self.get_object().center.slug)
        return context
