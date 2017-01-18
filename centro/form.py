from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from centro.models import Center, CenterService
from servicio.models import Service

class ServiceInline(ModelForm):
    class Meta:
        model = CenterService
        fields = ['center', 'service', 'cost', 'observation',]

class CenterCreateForm(ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'addres', 'geolocation',]

ServiceFormset = inlineformset_factory(Center, CenterService, fields = ('center', 'service', 'cost', 'observation'), extra=3, can_delete=False, can_order=True)