from django.db import models


class usuario(models.Model):
    
    username=models.CharField(max_length=40,default=False)
    password=models.CharField(max_length=255,default=False)
    nombre=models.CharField(max_length=40,default=False)
    apellidos=models.CharField(max_length=60,default=False)
    direccion=models.CharField(max_length=150,default=False)
    biografia=models.CharField(max_length=255,default=False)
    fechaNacimiento=models.DateField(default=False)
    fechaAlta=models.DateField(default=False)
    activo=models.SmallIntegerField(default=False)
    is_cliente = models.BooleanField('cliente status', default=False)
    is_empleado = models.BooleanField('empleado status', default=False)

    def __str__(self):
        return self.username

    
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
    idEmpleado: models.ForeignKey(usuario, on_delete=models.CASCADE)
    idCategoria: models.ForeignKey(categorias, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo


class participa(models.Model):
    
    idCliente: models.ForeignKey(usuario, on_delete=models.CASCADE)
    idProyecto: models.ForeignKey(proyectos, on_delete=models.CASCADE)
    fechaInscripcion: models.DateField()
    rol: models.CharField(max_length=100)
    
    def __str__(self):
        return self.fechaInscripcion