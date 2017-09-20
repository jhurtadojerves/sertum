from django import template
from datetime import date, timedelta

from servicio.models import Service
from centro.models import ServiceCenter

register = template.Library()


@register.filter(name='services')
def services(value):
    services = Service.objects.filter(center=value).distinct()
    return services


@register.filter(name='servicesMTM')
def servicesMTM(value):
    services = ServiceCenter.objects.filter(center=value)
    return services
