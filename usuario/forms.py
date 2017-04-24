from usuario.models import User as Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



from django import forms


class UsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'password': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

class ProfilePermission(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['reason_to_validate',]
        labels = ['Motivo para validar',]


