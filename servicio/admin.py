from django.contrib import admin

from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'center', 'slug',]
    list_editable = ['name',]

# Register your models here.
