from django import template
from datetime import date, timedelta

from servicio.models import Service

register = template.Library()

@register.filter(name='services')
def services(value):
    services = Service.objects.filter(center=value)
    return services