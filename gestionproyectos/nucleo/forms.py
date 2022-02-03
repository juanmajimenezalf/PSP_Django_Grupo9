import datetime
from faulthandler import disable
from nucleo.models import *
from django import forms

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User

        fields= [
            'dni',
            'nombre',
            'apellidos',
            'username',
            'password',
            'direccion',
            'biografia',
            'is_empleado'
        
        ]
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'username' : 'Nombre de usuario',
            'password' : 'Contraseña',
            'direccion': 'Direccion',
            'is_empleado' : 'empleado'
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}), 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'is_empleado':forms.BooleanField(required=False, initial=True),
            
        }
class ClienteForm(forms.ModelForm):
    
    class Meta:
        model = User

        fields= [
            'dni',
            'nombre',
            'apellidos',
            'username',
            
            'direccion',
            'fechaNacimiento',
           
            
        ]
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'username' : 'Nombre de usuario',
            
            'direccion': 'Direccion',
            'fechaNacimiento': 'Fecha de Nacimiento',
            'fechaAlta': 'Fecha de Alta',
            'is_cliente':'cliente'
            
            
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}), 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'fechaNacimiento': forms.DateInput(attrs={'class':'form-control'}),
            'fechaAlta':forms.DateField(required=False, initial=datetime.today),
            'is_cliente':forms.BooleanField(required=False, initial=True),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            
        }


class EditUserForm(forms.ModelForm):
    
    class Meta:
        model = User

        fields= [
            'dni',
            'first_name',
            'last_name',
            'username',
            
            'direccion',
            'username',
            'biografia',
        ]
        labels = {
            'dni': 'DNI',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'username' : 'Nombre de usuario',
            
            'direccion': 'Direccion',
            'username' : 'Username',
            
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}), 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
        }
class proyectosForm(forms.ModelForm):
    
    class Meta:
        model = proyectos

        fields= [
            'titulo',
            'descripcion',
            'nivel',
            'fechainicion',
            'fechafin',
            'informeFinal',
            'idEmpleado',
            'idCategoria',
        ]
        labels = {
            'titulo': 'Titulo',
            'descripcion': 'descripcion',
            'nivel': 'nivel',
            'fechainicion' : 'fechainicion',
            'fechafin' : 'fechafin',
            'informeFinal':'informeFinal',
            'idEmpleado': 'idEmpleado',
            'idCategoria' : 'idCategoria'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}), 
            'informeFinal': forms.TextInput(attrs={'class':'form-control'}), 
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'nivel': forms.NumberInput(attrs={'class':'form-control'}),
            'fechainicion': forms.DateInput(attrs={'class':'form-control'}),
            'fechafin': forms.DateInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
        }