from django.contrib import admin
from centro.models import Center, CenterService, Service
from django.forms.widgets import TextInput

# Register your models here.

from django_google_maps.widgets import GoogleMapsAddressWidget
from django_google_maps.fields import AddressField, GeoLocationField

class CenterServiceInline(admin.TabularInline):
    model = CenterService
    raw_id_fields = ('service',)
    extra = 1

@admin.register(Center)
class AdminCenter(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
    }
    inlines =(CenterServiceInline,)



