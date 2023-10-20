from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Producto
from .forms import ProductoForm
from django.urls import reverse_lazy

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'crear_producto.html'
    form_class = ProductoForm
    success_url = reverse_lazy('lista_productos')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'editar_producto.html'
    form_class = ProductoForm
    success_url = reverse_lazy('lista_productos')

class ListaProductosView(ListView):
    model = Producto
    template_name = 'lista_productos.html'
    context_object_name = 'productos'
