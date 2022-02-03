from datetime import datetime
from enum import Flag
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from nucleo.decorators import clienteTrue
import datetime
from nucleo.forms import UserForm, EditUserForm, proyectosForm, ClienteForm


from nucleo.forms import UserForm, EditUserForm, proyectosForm, ClienteForm, categoriasForm
from nucleo.models import User,proyectos,participa,categorias


def home(request):
    cliente=User.objects.filter(is_cliente=True)
    empleado=User.objects.filter(is_empleado=True)
    
    context={'empleado':empleado,
    'clientes':cliente,
 
    
    }
    return render(request, 'nucleo/home.html')
@method_decorator(staff_member_required, name='dispatch')
class empleadoCreate(CreateView):
    model = User
    
    form_class = UserForm
    template_name = 'nucleo/Empleado/create.html'
    success_url = reverse_lazy('nucleo:empleados')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            empleado=form.save(commit=False)
            empleado.is_empleado = True
            empleado.is_active = True
            empleado.save()
        return render(request, 'nucleo/Empleado/index.html', {'form':form})
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
def crearEmpleado(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            form.save()
        return redirect('nucleo:empleados')
    else:
        form = UserForm()

    return render(request, 'nucleo/Empleado/create.html', {'form':form})
def verEmpleados(request):
    empleado=User.objects.filter(is_empleado=True)
    context={'empleado':empleado}
    return render(request, 'nucleo/Empleado/index.html',context)

def editarEmpleado(request, id):
    empleado = User.objects.get(id=id)
    if request.method == 'GET':
        form = EditUserForm(instance=empleado)
    else:
        form = EditUserForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
        return redirect('nucleo:empleados')
    return render(request, 'nucleo/Empleado/create.html', {'form':form})

@method_decorator(staff_member_required, name='dispatch')
class EmpleadoUpdate (UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'nucleo/Empleado/create.html'
    success_url = reverse_lazy('nucleo:empleados')

def activateCliente(request, pk):
    cliente = User.objects.get(id=pk)
    cliente.is_active=True
    cliente.save()
    return redirect('nucleo:Clientes')
def borrarEmpleado(request, id):
    empleado = User.objects.get(id=id)
    empleado.delete()
    return redirect('nucleo:empleados')

@method_decorator(staff_member_required, name='dispatch')
class EmpleadoDelete(DeleteView):
    model = User
    template_name = "nucleo/Empleado/delete.html"
    success_url = reverse_lazy('nucleo:empleados')
    
@method_decorator(staff_member_required, name='dispatch')
class clienteCreate(CreateView):
    model = User
    
    form_class = ClienteForm
    template_name = 'nucleo/Cliente/create.html'
    success_url = reverse_lazy('nucleo:Clientes')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            cliente=form.save(commit=False)
            cliente.fechaAlta = datetime.date.today()
            cliente.is_active=False
            cliente.is_cliente = True
            cliente.save()
        return render(request, 'nucleo/Cliente/index.html', {'form':form})
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
def crearCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()   
        return redirect('nucleo:Clientes')
    else:
        
        form = ClienteForm()
        

    return render(request, 'nucleo/Cliente/create.html', {'form':form})
def verCliente(request):
    cliente=User.objects.filter(is_cliente=True)
    context={'cliente':cliente}
    return render(request, 'nucleo/Cliente/index.html',context)

def editarCliente(request, id):
    cliente = User.objects.get(id=id)
    if request.method == 'GET':
        form = ClienteForm(instance=cliente)
    else:
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
        return redirect('nucleo:Clientes')
    return render(request, 'nucleo/Cliente/create.html', {'form':form})

@method_decorator(staff_member_required, name='dispatch')
class ClienteUpdate (UpdateView):
    model = User
    form_class = ClienteForm
    template_name = 'nucleo/Cliente/create.html'
    success_url = reverse_lazy('nucleo:Clientes')

def borrarCliente(request, id):
    cliente = User.objects.get(id=id)
    cliente.delete()
    return redirect('nucleo:Clientes')

@method_decorator(staff_member_required, name='dispatch')
class ClienteDelete(DeleteView):
    model = User
    template_name = "nucleo/Cliente/delete.html"
    success_url = reverse_lazy('nucleo:Clientes')
    
    
    
@method_decorator(staff_member_required, name='dispatch')
class proyectoCreate(CreateView):
    model = proyectos
    
    form_class = proyectosForm
    template_name = 'nucleo/Empleado/create.html'
    success_url = reverse_lazy('nucleo:home')
def verProyectos(request):
    empleado=proyectos.objects.filter(is_empleado=True)
    context={'empleado':empleado}
    return render(request, 'nucleo/Proyectos/index.html',context)

class categoriasCreate(CreateView):
    model = categorias
    form_class= categoriasForm
    template_name = 'nucleo/categoria.html'
    success_url = reverse_lazy('nucleo:home')