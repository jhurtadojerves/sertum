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
        fields = ['name', 'addres', 'aditional_information', ]
        widgets = {
            'name': forms.TextInput()
        }


class CenterUpdateForm(ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'addres', 'aditional_information', ]

        widgets = {
            'name': forms.TextInput()
        }

class PictureCreateForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture', 'center',]


class PictureAddForm(forms.Form):
    picture = forms.FileField(label="Seleccionar una imagen")


class KnowledgePollForm(forms.Form):
    group_type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                queryset=GroupTypeForKnowledge.objects.all(), label='Conformación del grupo de Turistas', required=True)
    activity = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              queryset=ActivityForKnowledge.objects.all(), required=True,
                                              label='Actividades que desea desarrollar')
    transport = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=TransportForKnowledge.objects.all(), required=True,
                                               label='Método de transporte preferido')
    food = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=FoodForKnowledge.objects.all(),
                                  required=True, label='Comida preferida')
    money_per_people = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0, required=True,
                                          label='Dinero máximo por persona')


class KnowledgeCreate(ModelForm):
    class Meta:
        model = Knowledge
        fields = ('group_type', 'money_per_person', 'activities', 'transport', 'food', )
        widgets = {
            'group_type': forms.CheckboxSelectMultiple(),
            'activities': forms.CheckboxSelectMultiple(),
            'transport': forms.CheckboxSelectMultiple(),
            'food': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'group_type': 'Grupo de personas que pueden visitar el Destino',
            'money_per_person': 'Gasto aproximado de una persona',
            'activities': 'Actividades que se pueden realizar',
            'transport': 'Medio de Transporte disponible',
            'food': 'Tipo de comida que ofrece',
        }
