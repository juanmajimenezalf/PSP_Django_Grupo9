
from enum import Flag
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView,DeleteView, ListView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from nucleo.decorators import clienteTrue, empleadoTrue, noAdmin
from datetime import datetime
from nucleo.forms import UserForm, EditUserForm, proyectosForm, ClienteForm, categoriasForm
from nucleo.models import User,Proyectos,Participa,Categorias
from django.contrib import messages


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
            empleado.is_active = False
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
            cliente.is_active = False
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
@method_decorator(empleadoTrue, name='dispatch')
class proyectoCreate(CreateView):
    model = Proyectos
    form_class = proyectosForm
    template_name = 'nucleo/Proyectos/create.html'  
    success_url = reverse_lazy('Proyecto:indexProyectos') 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.idEmpleado = User.objects.filter(pk=self.request.user.id).first()
            proyecto.save()
            messages.success(request, 'Proyecto registrado')
            return HttpResponseRedirect(reverse('nucleo:indexProyectos'))
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
@method_decorator(empleadoTrue, name='dispatch')
class proyectoUpdate(UpdateView):
    model=Proyectos
    form_class = proyectosForm
    template_name = 'nucleo/Proyectos/create.html'
    success_url = reverse_lazy('nucleo:indexProyectos')
@method_decorator(empleadoTrue, name='dispatch')
class proyectoDelete(DeleteView):
    model= Proyectos
    template_name = 'nucleo/Proyectos/delete.html'
    success_url = reverse_lazy('nucleo:indexProyectos')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return  super().dispatch(request, *args, **kwargs)
        


@noAdmin
def verProyectos(request):
    proyectos=Proyectos.objects.all()
    context={'proyectos':proyectos}
    return render(request, 'nucleo/Proyectos/index.html', context)

@clienteTrue
def ParticipaCreate(request,pk):
    AlredyIns = Participa.objects.filter(idProyecto_id=pk).filter(idCliente_id=request.user.id).exists()
    print(AlredyIns)
    proyectos=Proyectos.objects.all()
    proyecto = Proyectos.objects.filter(pk=pk).first()
    user = User.objects.filter(pk=request.user.id).first()
    participa = Participa.objects.all()
    if (AlredyIns == True ):
        context={'proyectos':proyectos,
                'user':user,
                'participa': participa}
        print('SI')
        
        messages.success(request, 'Ya estás inscrito en esa oferta')
        return render(request, 'nucleo/Proyectos/index.html', context)
    else:
        if proyecto is not None:
            print('NO')
            inscripcion = Participa()
            inscripcion.idCliente = user
            inscripcion.idProyecto = proyecto
            inscripcion.fechaInscripcion = datetime.date.today()
            inscripcion.save()

        context={'proyectos':proyectos,
                'user':user,
                'participa': participa}
        return render(request, 'nucleo/Proyectos/index.html', context)
    
@method_decorator(staff_member_required, name='dispatch')
class categoriaCreate(CreateView):
    model = Categorias
    form_class= categoriasForm
    template_name = 'nucleo/Categorias/create.html'
    success_url = reverse_lazy('nucleo:indexCategoria')

@method_decorator(staff_member_required, name='dispatch')
class categoriaUpdate(UpdateView):
    model = Categorias
    form_class = categoriasForm
    template_name = 'nucleo/Categorias/create.html'
    success_url = reverse_lazy('nucleo:indexCategoria')

@method_decorator(staff_member_required, name='dispatch')
class categoriaDelete(DeleteView):
    model = Categorias
    template_name = 'nucleo/Categorias/delete.html'
    success_url = reverse_lazy('nucleo:indexCategoria')

    def post(self, request, *args, **kwargs):
        self.object.delete()
        messages.success(request, 'Categoría eliminada con éxito')
        return HttpResponseRedirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

@method_decorator(staff_member_required, name='dispatch')
def verCategorias(request):
    categorias=Categorias.objects.all()
    context={'categorias':categorias}
    return render(request, 'nucleo/Categorias/index.html', context) 

class historialProyectosE(ListView):
    model = Proyectos
    template_name = 'nucleo/Proyectos/historialProyectoE.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyectos'] = Proyectos.objects.filter(idEmpleado_id=self.request.user, fechafin__lt = datetime.now())
        return context

class historialProyectosC(ListView):
    model = Proyectos
    template_name = 'nucleo/Proyectos/historialProyectoC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyectos'] = Proyectos.objects.filter(participa__idCliente_id = self.request.user, fechafin__lt = datetime.now())
        return context

class clienteProyecto(ListView):
    model = Participa
    template_name = 'nucleo/Proyectos/misClientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Participa.objects.filter(idProyecto_id=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        Participa.objects.filter(idProyecto_id=self.kwargs.get('pk'),idCliente_id=self.request.POST.get('idCliente_id').update(rol=self.request.POST.get('rol')))
        return HttpResponseRedirect(reverse('nucleo:clienteProyecto'),kwargs={'pk':self.kwargs.get('pk')})