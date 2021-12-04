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

class empleados(models.Model):
    id = models.SmallIntegerField(auto_increment=True, primary_key=True)
    dni=models.CharField(max_length=9, unique=True)
    nombre=models.CharField(max_length=40)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=150)
    biografia=models.CharField(max_length=255)
    idUsuario=models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.dni
    
class participa(models.Model):
    id: models.SmallIntegerField(auto_increment=True, primary_key=True)
    idCliente: models.ForeignKey(cliente, on_delete=models.CASCADE)
    idProyecto: models.ForeignKey(proyectos, on_delete=models.CASCADE)
    fechaInscripcion: models.DateField()
    rol: models.CharField(max_length=100)
    
    def __str__(self):
        return self.fechaInscripcion
    
class proyectos(models.Model):
    id: models.SmallIntegerField(auto_increment=True, primary_key=True)
    titulo: models.charField(max_length=150)
    descripcion: models.CharField(max_length=255)
    nivel: models.IntegerField()
    fechainicion: models.DateField()
    fechafin: models.DateField()
    idEmpleado: models.ForeignKey(empleados, on_delete=models.CASCADE)
    idCategoria: models.ForeignKey(categorias, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class categorias(models.Model):
    id: models.SmallIntegerField(auto_increment=True, primary_key=True)
    nombre: models.charField(max_length=150)
    foto: models.charField(max_length=255)
    
    def __str__(self):
        return self.nombre
    
    