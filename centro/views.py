from django.shortcuts import render

from django.views.generic import DetailView

from .models import Center

# Create your views here.

class CenterDetailView(DetailView):
    model = Center
    template_name = 'center_detail.html'
    slug_field = 'slug'
    context_object_name = 'center'
