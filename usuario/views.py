from django.shortcuts import render

# Create your views here.

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context import RequestContext

from django.contrib.auth.mixins import PermissionRequiredMixin


from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from usuario.models import User as Profile


from .forms import UsuarioForm, ProfilePermission


from django.views.generic import CreateView, ListView, UpdateView



class RegisterUserCreateView(CreateView):
    model = User
    template_name = "registro.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('Center:home')

    def get_context_data(self, **kwargs):
        context = super(RegisterUserCreateView, self).get_context_data(**kwargs)
        context['verification'] = True
        context['request'] = self.request

        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.get_or_create(user = user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ValidationUserListView(PermissionRequiredMixin, ListView):
    permission_required = 'is_staff'
    model = Profile
    template_name = "validar.html"
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = self.model.objects.filter(has_add_center = False)
        return queryset


class AddPermissionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Profile
    template_name = 'add_permission.html'
    form_class = ProfilePermission
    context_object_name = 'usuario'
    success_url = 'User:listar_sin_permisos'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id = kwargs['pk']
        profile = self.model.objects.get(id=id)
        form = self.form_class(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save()
            profile.has_add_center = True
            permissions = Permission.objects.filter(codename='add_center')

            for permission in permissions:
                profile.user.user_permissions.add(permission)
            profile.save()
            return HttpResponseRedirect(reverse(self.get_success_url()))
        else:
            return self.render_to_response(self.get_context_data(form=form))





