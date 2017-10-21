from django.shortcuts import render

from django.views.generic import DetailView, CreateView, UpdateView, ListView, FormView, View

from .models import Center, Picture, Knowledge, Poll
from usuario.models import User as Usuario
from .form import CenterCreateForm, CenterUpdateForm, PictureCreateForm, PictureAddForm, KnowledgePollForm, KnowledgeCreate
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


class CenterCreateView(CreateView):
    model = Center
    template_name = 'center_create.html'
    form_class = CenterCreateForm
    context_object_name = 'center'

    @method_decorator(permission_required('usuario.add_center'))
    def dispatch(self, *args, **kwargs):
        return super(CenterCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        form.save()
        return super(CenterCreateView, self).form_valid(form)


class CenterUpdateView(UpdateView):
    model = Center
    template_name = 'center_edit.html'

    form_class = CenterUpdateForm
    context_object_name = 'center'

    def get_object(self, queryset=None):
        queryset = Center.objects.get(user=self.request.user.profile)
        return queryset


class CenterListView(ListView):
    model = Center
    template_name = 'center_list.html'
    context_object_name = 'centers'


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


class PollForm(FormView):
    template_name = "poll_form_2.html"
    form_class = KnowledgePollForm
    success_url = reverse_lazy('Center:encuesta_resultado')

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

        centervalue = list()
        for c in centers:
            value = 0
            center = c.center

            groups = set(c.group_type.all().values_list('name'))
            activities = set(c.activities.all().values_list('name'))
            transport = set(c.transport.all().values_list('name'))
            food = set(c.food.all().values_list('name'))

            money_per_person = c.money_per_person

            temp_g = groups & form_groups
            #comprobar(form, conocimiento) -> 3
            value += len(temp_g)

            temp_a = activities & form_activities
            value += len(temp_a)

            temp_t = transport & form_transport
            value += len(temp_t)

            temp_f = food & form_food
            value += len(temp_f)

            if money_per_person <= form_money_per_person:
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


class PollResult(DetailView):
    model = Poll
    template_name = "poll_result.html"
    context_object_name = 'poll'


class CreateKnowledge(PermissionRequiredMixin, CreateView):
    permission_required = "usuario.add_center"
    model = Knowledge
    template_name = "knowledge_create.html"
    form_class = KnowledgeCreate

    def form_valid(self, form):
        user = Usuario.objects.get(user=self.request.user)
        center = Center.objects.get(user=user)
        form.instance.center = center
        form.save()
        return super(CreateKnowledge, self).form_valid(form)

    def get_success_url(self):
        return reverse('Center:center_detail', args=[self.request.user.profile.center.slug])

    def dispatch(self, request, *args, **kwargs):
        if Knowledge.objects.filter(center=request.user.profile.center).exists():
            return HttpResponseRedirect(reverse_lazy('Center:knowledge_update'))
        else:
            return super(CreateKnowledge, self).dispatch(request, *args, **kwargs)


class UpdateKnowledge(PermissionRequiredMixin, UpdateView):
    permission_required = "usuario.add_center"
    model = Knowledge
    template_name = "knowledge_update.html"
    form_class = KnowledgeCreate

    def get_object(self, queryset=None):
        queryset = Knowledge.objects.get(center=self.request.user.profile.center)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not Knowledge.objects.filter(center=request.user.profile.center).exists():
            return HttpResponseRedirect(reverse_lazy('Center:knowledge_create'))
        else:
            return super(UpdateKnowledge, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('Center:center_detail', args=[self.request.user.profile.center.slug])
