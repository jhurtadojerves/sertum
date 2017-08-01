from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from centro.models import Center, Picture, Knowledge, Poll
from servicio.models import Service
from django import forms

from django import forms


class CenterCreateForm(ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'addres', 'geolocation', 'user', 'aditional_information',]


class PictureCreateForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture', 'center',]


class PictureAddForm(forms.Form):
    picture = forms.FileField(label="Seleccionar una imagen")


class KnowledgePollForm(forms.Form):
    group_type_choices = (
        ('0', 'Niños'),
        ('1', 'Adultos'),
        ('2', 'Adultos Mayores'),
    )
    group_type = forms.ChoiceField(choices=group_type_choices)
