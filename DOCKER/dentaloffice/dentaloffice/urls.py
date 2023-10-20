"""
URL configuration for dentaloffice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pacientes import views as pacientes_views
from productos import views as productos_views
from prescripcion import views as prescripcion_views
from compras import views as compras_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', pacientes_views.CustomLoginView.as_view()),
    path('pacientes/create/', pacientes_views.registrar_paciente, name= 'registrar_paciente'),
    path('pacientes/', pacientes_views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/<int:pk>/editar/', pacientes_views.PacienteUpdateView.as_view(), name='editar_paciente'),

    path('productos/create/', productos_views.ProductoCreateView.as_view(), name='crear_producto'),
    path('productos/<int:pk>/editar/', productos_views.ProductoUpdateView.as_view(), name='editar_producto'),
    path('productos/', productos_views.ListaProductosView.as_view(), name='lista_productos'),

    path('prescripciones/create/', prescripcion_views.registrar_prescripcion, name='registrar_prescripcion'),
    path('prescripciones/', prescripcion_views.lista_prescripciones, name='lista_prescripciones'),
    path('prescripciones/<int:pk>/', prescripcion_views.actualizar_prescripcion, name='actualizar_prescripcion'),

    path('compras/create/', compras_views.registrar_compra)

]
