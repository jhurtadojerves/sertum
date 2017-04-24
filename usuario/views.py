from django.shortcuts import render

# Create your views here.

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context import RequestContext



from django.contrib.auth.mixins import PermissionRequiredMixin


from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from usuario.models import User as Profile
from centro.models import Center



from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from .forms import UsuarioForm, ProfilePermission


from django.views.generic import CreateView, ListView, UpdateView, FormView, RedirectView




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

class UserLogin(FormView):
    model = User
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("Center:home")
    redirect_field_name = REDIRECT_FIELD_NAME


    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()

        return super(UserLogin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(UserLogin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context =  super(UserLogin, self).get_context_data(**kwargs)


        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = Profile.objects.filter(user = self.request.user)
            center = Center.objects.filter(user=user)
            if center.exists():
                context['verification'] = False
                context['center_view'] = Center.objects.get(user=user)
            else:
                context['verification'] = True
        else:
            context['verification'] = True


        return context

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('User:login')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)