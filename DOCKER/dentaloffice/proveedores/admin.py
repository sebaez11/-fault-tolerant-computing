from django.contrib import admin
from .models import Proveedor
from .forms import ProveedorForm

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'email', 'telefono')
    search_fields = ('nombre', 'email')
    form = ProveedorForm

admin.site.register(Proveedor, ProveedorAdmin)
