from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from centro.models import Center, Picture, Knowledge, Poll
from servicio.models import Service

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


class KnowledgePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['group_type', 'money_per_person', 'activities', 'transport', 'food', 'extreme_sport', 'sport_fishing', 'night_bar', 'has_lodging']