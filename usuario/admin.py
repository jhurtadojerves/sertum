from django.contrib import admin
from  usuario.models import User as Usuario

@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_full_name']

# Register your models here.
