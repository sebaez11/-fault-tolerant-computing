from django.contrib import admin
from .forms import UsuarioCreationForm
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre' , 'email' , 'username', 'role' , 'direccion')
    search_fields = ('nombre', 'email', 'username')
    form = UsuarioCreationForm

admin.site.register(Usuario, UsuarioAdmin)