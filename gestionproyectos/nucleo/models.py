from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    username = models.CharField(max_length=40, unique=True, null=True)
    dni = models.CharField(max_length=9, unique=True, null=True)
    password = models.CharField(max_length=255, null=True)
    nombre = models.CharField(max_length=40, null=True)
    apellidos = models.CharField(max_length=60, null=True)
    direccion = models.CharField(max_length=150, null=True)
    biografia = models.CharField(max_length=255, null=True)
    fechaNacimiento = models.DateField(null=True)
    fechaAlta = models.DateField(datetime.today)
    activo = models.SmallIntegerField( null=True)
    is_cliente = models.BooleanField('cliente status', null=True)
    is_empleado = models.BooleanField('empleado status', null=True)

    def __str__(self):
        return self.username

    
class Categorias(models.Model):
       
    nombre = models.CharField(max_length=150, null=True)
    foto = models.ImageField(upload_to='images/',verbose_name="foto", null=True)
    
    def __str__(self):
        return self.nombre
        
class Proyectos(models.Model):
    
    titulo = models.CharField(max_length=150, null=True)
    descripcion = models.CharField(max_length=255, null=True)
    nivel = models.IntegerField(null=True)
    fechainiciacion = models.DateField(null=True)
    fechafin = models.DateField(null=True)
    informeFinal = models.CharField(max_length=150, null=True)
    idEmpleado = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    idCategoria = models.ForeignKey(Categorias, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return str(self.titulo)


class Participa(models.Model):
    
    idCliente = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    idProyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE,null=True)
    fechaInscripcion = models.DateField(null=True)
    rol = models.CharField(max_length=100,null=True)
    
    def __int__(self):
        return self.id