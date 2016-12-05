from django.contrib import admin
from centro.models import Center
from django.forms.widgets import TextInput

# Register your models here.

from django_google_maps.widgets import GoogleMapsAddressWidget
from django_google_maps.fields import AddressField, GeoLocationField


@admin.register(Center)
class AdminCenter(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
    }



