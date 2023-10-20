from .models import Prescripcion, PrescripcionProducto
from django.forms import modelformset_factory
from django import forms


class PrescripcionForm(forms.ModelForm):
    class Meta:
        model = Prescripcion
        fields = ['paciente', 'fecha']

class PrescripcionProductoForm(forms.ModelForm):
    class Meta:
        model = PrescripcionProducto
        fields = ['producto', 'nota']

PrescripcionProductoFormSet = modelformset_factory(PrescripcionProducto, form=PrescripcionProductoForm, extra=1)