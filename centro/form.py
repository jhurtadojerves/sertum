from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from centro.models import Center, Picture, Knowledge, Poll, ActivityForKnowledge, GroupTypeForKnowledge, FoodForKnowledge, TransportForKnowledge
from servicio.models import Service
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

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
    group_type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=GroupTypeForKnowledge.objects.all(), required=True)
    activity = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              queryset=ActivityForKnowledge.objects.all(), required=True,
                                              label='Actividades que desea desarrollar')
    transport = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=TransportForKnowledge.objects.all(), required=True,
                                               label='Método de transporte preferido')
    food = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=FoodForKnowledge.objects.all(),
                                  required=True, label='Comida preferida')
    money_per_people = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0, required=True,
                                          label='Dinero máximo por persona')
    #extreme_sport = forms.BooleanField(required=None, label='¿Desea practicar deportes extremos?')
    #sport_fishing = forms.BooleanField(required=None, label='¿Desea realizar pesca deportiva?')
    #night_bar = forms.BooleanField(required=None, label='¿Desea visitar un bar o discoteca?')
    #has_lodging = forms.BooleanField(required=None, label='¿Necesita hospedaje en el destino turístico?')
