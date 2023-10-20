from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.PositiveIntegerField()
    stock_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre