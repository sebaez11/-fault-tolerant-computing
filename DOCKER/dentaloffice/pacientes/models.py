from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.nombre
    
class ContactoEmergencia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='contactos_emergencia')
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    parentesco = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre