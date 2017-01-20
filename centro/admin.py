from django.contrib import admin
from centro.models import Center, CenterService, Service, Picture
from django.forms.widgets import TextInput

# Register your models here.

from django_google_maps.widgets import GoogleMapsAddressWidget
from django_google_maps.fields import AddressField, GeoLocationField

class CenterServiceInline(admin.TabularInline):
    model = CenterService
    raw_id_fields = ('service',)
    extra = 1
class PictureInline(admin.TabularInline):
    model = Picture

@admin.register(Center)
class AdminCenter(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'user' ]
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
    }
    inlines =[
        CenterServiceInline,
        PictureInline,
    ]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'picture',
        'center',
    ]


