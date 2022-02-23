from rest_framework import serializers
from nucleo.models import User, Proyectos, Categorias

class CategoriaSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Categorias
        fields=['nombre','foto']

class ClienteSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=['dni','nombre','apellidos','direccion','fechaNacimiento','fechaAlta']
class EmpleadoSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=['dni','nombre','apellidos','direccion','biografia']

class ProyectosSerializers(serializers.ModelSerializer):
    
    idEmpleado = EmpleadoSerializers(read_only=True)
    idCategoria = CategoriaSerializers(read_only=True)

    class Meta:
        model = Proyectos
        fields=['titulo','descripcion','nivel','fechainiciacion','fechafin','informeFinal','idEmpleado','idCategoria']

class ParticipaSerializers(serializers.ModelSerializer):
    
    idCliente = ClienteSerializers(read_only=True)
    idProyecto = ProyectosSerializers(read_only=True)

    class Meta:
        model = User
        fields=['idCliente','idProyecto','fechainscripcion','rol']

