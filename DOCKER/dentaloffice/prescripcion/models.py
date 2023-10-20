from django.db import models
from productos.models import Producto
from pacientes.models import Paciente

class Prescripcion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    productos = models.ManyToManyField(Producto, through='PrescripcionProducto')

    def __str__(self):
        return f"Prescripción para {self.paciente} - {self.fecha}"


class PrescripcionProducto(models.Model):
    prescripcion = models.ForeignKey(Prescripcion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nota = models.TextField(blank=True)

    def __str__(self):
        return f"{self.prescripcion} - {self.producto}"
