from django.db import models
from django.db.models.constraints import UniqueConstraint

class usuario(models.Model):
    
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.username

class cliente(models.Model):
    
    dni=models.CharField(max_length=9, unique=True)
    nombre=models.CharField(max_length=40)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=150)
    fechaNacimiento=models.DateField()
    fechaAlta=models.DateField(auto_now_add=True)
    activo=models.SmallIntegerField()
    idUsuario=models.ForeignKey(usuario, on_delete=models.CASCADE)


    def __str__(self):
        return self.dni

class empleados(models.Model):
   
    dni=models.CharField(max_length=9, unique=True)
    nombre=models.CharField(max_length=40)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=150)
    biografia=models.CharField(max_length=255)
    idUsuario=models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.dni
    
class categorias(models.Model):
       
    nombre: models.CharField(max_length=150)
    foto: models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
        
class proyectos(models.Model):
    
    titulo: models.CharField(max_length=150)
    descripcion: models.CharField(max_length=255)
    nivel: models.IntegerField()
    fechainicion: models.DateField()
    fechafin: models.DateField()
    idEmpleado: models.ForeignKey(empleados, on_delete=models.CASCADE)
    idCategoria: models.ForeignKey(categorias, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo


class participa(models.Model):
    
    idCliente: models.ForeignKey(cliente, on_delete=models.CASCADE)
    idProyecto: models.ForeignKey(proyectos, on_delete=models.CASCADE)
    fechaInscripcion: models.DateField()
    rol: models.CharField(max_length=100)
    
    def __str__(self):
        return self.fechaInscripcion