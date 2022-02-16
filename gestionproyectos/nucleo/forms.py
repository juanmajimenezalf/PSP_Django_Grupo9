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
            
        
        ]
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'username' : 'Nombre de usuario',
            'password' : 'Contraseña',
            'direccion': 'Direccion',
           
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}), 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            
            
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
            
            
            
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control'}), 
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'fechaNacimiento': forms.DateInput(attrs={'class':'form-control'}),
            
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
        model = Proyectos

        fields= [
            'titulo',
            'descripcion',
            'nivel',
            'fechainiciacion',
            'fechafin',
            'informeFinal',
            
            'idCategoria',
        ]
        labels = {
            'titulo': 'Titulo',
            'descripcion': 'descripcion',
            'nivel': 'nivel',
            'fechainiciacion' : 'fechainiciacion',
            'fechafin' : 'fechafin',
            'informeFinal':'informeFinal',
            
            'idCategoria' : 'Categoría'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}), 
            'informeFinal': forms.Textarea(attrs={'class':'form-control'}), 
            'descripcion': forms.Textarea(attrs={'class':'form-control'}),
            'nivel': forms.NumberInput(attrs={'class':'form-control'}),
            'fechainicion': forms.DateInput(attrs={'class':'form-control'}),
            'fechafin': forms.DateInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
        }

class categoriasForm(forms.ModelForm):
    class Meta:
        model=Categorias
        
        fields= [
            'nombre',
            'foto',            
        ]
        
        labels={
            'nombre': 'Nombre',
            'foto': 'Foto',
        }
        
        Widgets={
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'foto': forms.FileInput()
        }