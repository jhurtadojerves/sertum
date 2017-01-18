from django.contrib import admin
from  usuario.models import User as Usuario

@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'user', 'as_premium']

# Register your models here.
