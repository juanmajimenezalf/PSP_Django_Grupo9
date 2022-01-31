from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=255)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    biografia = models.CharField(max_length=255)
    fechaNacimiento = models.DateField()
    fechaAlta = models.DateField(auto_now_add=True)
    activo = models.SmallIntegerField()
    is_cliente = models.BooleanField('cliente status')
    is_empleado = models.BooleanField('empleado status')

    def __str__(self):
        return self.username

    
class categorias(models.Model):
       
    nombre = models.CharField(max_length=150)
    foto = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
        
class proyectos(models.Model):
    
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=255)
    nivel = models.IntegerField()
    fechainicion = models.DateField()
    fechafin = models.DateField()
    idEmpleado = models.ForeignKey(User, on_delete=models.CASCADE)
    idCategoria = models.ForeignKey(categorias, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo


class participa(models.Model):
    
    idCliente = models.ForeignKey(User, on_delete=models.CASCADE)
    idProyecto = models.ForeignKey(proyectos, on_delete=models.CASCADE)
    fechaInscripcion = models.DateField()
    rol = models.CharField(max_length=100)
    
    def __str__(self):
        return self.fechaInscripcion