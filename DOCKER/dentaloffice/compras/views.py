from django.shortcuts import render, redirect
from .models import Compra
from .forms import CompraForm

def registrar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save()
            # Redirige a la página de detalles de la compra u otra vista según tus necesidades.
            return redirect('detalle_compra', compra_id=compra.id)
    else:
        form = CompraForm()
    
    return render(request, 'registrar_compra.html', {'form': form})
