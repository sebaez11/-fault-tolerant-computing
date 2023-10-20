from .models import Paciente, ContactoEmergencia
from django.forms import inlineformset_factory
from django import forms


ContactoEmergenciaFormSet = inlineformset_factory(Paciente, ContactoEmergencia, fields=('nombre', 'telefono', 'parentesco'), extra=1)

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'direccion', 'email']

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
