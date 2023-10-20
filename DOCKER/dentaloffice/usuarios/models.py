from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    
    # Agrega related_name a las relaciones de grupos y permisos
    groups = models.ManyToManyField(Group, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios')

    def __str__(self):
        return self.nombre
