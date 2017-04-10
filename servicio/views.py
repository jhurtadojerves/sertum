from django.shortcuts import render

from django.views.generic import CreateView

from .models import Service
from usuario.models import User as Usuario
from centro.models import Center

# Create your views here.


class CreateServiceView(CreateView):
    model = Service
    template_name = "service_create.html"
    context_object_name = "service"
    fields = ['name', 'center', 'cost', 'observation', ]


    def get_context_data(self, **kwargs):
        context = super(CreateServiceView, self).get_context_data(**kwargs)
        context['request'] = self.request
        user = Usuario.objects.get(user=self.request.user)
        center = Center.objects.filter(user=user)
        if center.exists():
            context['verification'] = False
            context['center'] = Center.objects.get(user=user)
        else:
            context['verification'] = True

        return context
