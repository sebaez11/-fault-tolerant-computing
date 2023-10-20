from django.db import models
from productos.models import Producto  # Asegúrate de importar tu modelo de Producto si aún no lo has hecho

class Compra(models.Model):
    fecha = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    productos = models.ManyToManyField(Producto, through='CompraProducto')


class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
