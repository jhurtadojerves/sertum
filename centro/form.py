from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from centro.models import Center
from servicio.models import Service



class CenterCreateForm(ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'addres', 'geolocation', 'user', 'aditional_information',]