from django.contrib import admin
from centro.models import Center, Picture
from servicio.models import Service
from django.forms.widgets import TextInput

# Register your models here.

from django_google_maps.widgets import GoogleMapsAddressWidget
from django_google_maps.fields import AddressField, GeoLocationField


class PictureInline(admin.TabularInline):
    model = Picture

class ServiceInline(admin.TabularInline):
    model = Service


@admin.register(Center)
class AdminCenter(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'user', 'addres', ]
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
    }
    inlines =[
        PictureInline,
        ServiceInline,
    ]

    list_editable = ['user',]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'picture',
        'center',
    ]


