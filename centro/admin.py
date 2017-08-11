from django.contrib import admin
from centro.models import Center, Picture, Knowledge, Poll, ActivityForKnowledge, FoodForKnowledge, GroupTypeForKnowledge, TransportForKnowledge
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
    ]

    list_editable = ['user',]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'picture',
        'center',
    ]

@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'center']

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'center', 'value', 'date']


@admin.register(ActivityForKnowledge)
class ActivityForKnowledge(admin.ModelAdmin):
    list_display = ['name']


@admin.register(GroupTypeForKnowledge)
class GroupTypeForKnowledgeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FoodForKnowledge)
class FoodForKnowledge(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TransportForKnowledge)
class TransportForKnowledge(admin.ModelAdmin):
    list_display = ['name']