from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Paciente

# Forms
from .forms import PacienteForm, ContactoEmergenciaFormSet

class CustomLoginView(LoginView):
    template_name = 'login.html'


class PacienteUpdateView(UpdateView):
    model = Paciente
    template_name = 'editar_paciente.html'  # Crea una plantilla para la edición
    fields = ['nombre', 'direccion', 'email']
    success_url = reverse_lazy('lista_pacientes')  # Redirige a la lista de pacientes después de la edición

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        contacto_formset = ContactoEmergenciaFormSet(request.POST, prefix='contacto')

        if form.is_valid() and contacto_formset.is_valid():
            paciente = form.save()

            contacto_emergencia = contacto_formset.save(commit=False)
            for contacto in contacto_emergencia:
                contacto.paciente = paciente
                contacto.save()

            return redirect('pagina_de_exito')  # Redirige a la página de éxito
    else:
        form = PacienteForm()
        contacto_formset = ContactoEmergenciaFormSet(prefix='contacto')

    return render(request, 'registrar_paciente.html', {'form': form, 'contacto_formset': contacto_formset})

