from django.db import models
from django.db.models.constraints import UniqueConstraint

class usuario(models.Model):
    id = models.SmallIntegerField(auto_increment=True, primary_key=True)
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.dni

class cliente(models.Model):
    id = models.SmallIntegerField(auto_increment=True, primary_key=True)
    dni=models.CharField(max_length=9, unique=True)
    nombre=models.CharField(max_length=40)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=150)
    fechaNacimiento=models.DateField()
    fechaAlta=models.DateField()
    activo=models.SmallIntegerField()
    idUsuario=models.ForeignKey(usuario, on_delete=models.CASCADE)


    def __str__(self):
        return self.dni

class empleado(models.Model):
    id = models.SmallIntegerField(auto_increment=True, primary_key=True)
    dni=models.CharField(max_length=9, unique=True)
    nombre=models.CharField(max_length=40)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=150)
    biografia=models.CharField(max_length=255)
    idUsuario=models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.dni