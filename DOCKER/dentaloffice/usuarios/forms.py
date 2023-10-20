from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('dentista', 'Dentista'),
        ('recepcionista', 'Recepcionista'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'role', 'direccion', 'email', 'username']
