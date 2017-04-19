from django.shortcuts import render

# Create your views here.

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from usuario.models import User as Profile


from .forms import UsuarioForm


from django.views.generic import CreateView



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
            user.is_active = 0
            profile = Profile.objects.get_or_create(user = user)
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))