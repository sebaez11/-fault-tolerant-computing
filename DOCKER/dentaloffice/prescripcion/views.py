from django.shortcuts import render, redirect
from .models import Prescripcion, PrescripcionProducto
from .forms import PrescripcionForm, PrescripcionProductoForm, PrescripcionProductoFormSet

def registrar_prescripcion(request):
    if request.method == 'POST':
        form = PrescripcionForm(request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir a una página de éxito o hacer algo más aquí
            # return redirect('pagina_de_exito')
    else:
        form = PrescripcionForm()
    
    return render(request, 'registrar_prescripcion.html', {'form': form})

def lista_prescripciones(request):
    prescripciones = Prescripcion.objects.all()
    return render(request, 'lista_prescripciones.html', {'prescripciones': prescripciones})

def actualizar_prescripcion(request, pk):
    prescripcion = Prescripcion.objects.get(pk=pk)

    if request.method == 'POST':
        prescripcion_form = PrescripcionForm(request.POST, instance=prescripcion)
        producto_formset = PrescripcionProductoFormSet(request.POST, prefix='producto', instance=prescripcion)

        if prescripcion_form.is_valid() and producto_formset.is_valid():
            prescripcion_form.save()
            producto_formset.save()

            return redirect('lista_prescripciones')  # Redirige a la lista de prescripciones
    else:
        prescripcion_form = PrescripcionForm(instance=prescripcion)
        producto_formset = PrescripcionProductoFormSet(prefix='producto', instance=prescripcion)

    return render(request, 'actualizar_prescripcion.html', {
        'prescripcion_form': prescripcion_form,
        'producto_formset': producto_formset,
        'prescripcion': prescripcion,
    })
