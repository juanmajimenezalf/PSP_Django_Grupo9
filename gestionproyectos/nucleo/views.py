
from enum import Flag
from re import I
import string
from tkinter import N
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
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
    success_url = reverse_lazy('nucleo:indexEmpleado')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            empleado=form.save(commit=False)
            empleado.fechaAlta = datetime.today()
            empleado.is_empleado = True
            empleado.set_password(form.cleaned_data["password"])
            empleado.is_active = True
            empleado.save()
        return redirect('nucleo:indexEmpleado')
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
@staff_member_required
def borrarEmpleado(request, pk):
    empleado = User.objects.get(id=pk)
    empleado.delete()
    return redirect('nucleo:indexEmpleado')

@staff_member_required
def verEmpleados(request):
    empleado=User.objects.filter(is_empleado=True)
    context={'empleado':empleado}
    return render(request, 'nucleo/Empleado/index.html',context)


@method_decorator(staff_member_required, name='dispatch')
class EmpleadoUpdate (UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'nucleo/Empleado/create.html'
    success_url = reverse_lazy('nucleo:indexEmpleado')




@method_decorator(staff_member_required, name='dispatch')
class clienteCreate(CreateView):
    model = User
    form_class = ClienteForm
    template_name = 'nucleo/Cliente/create.html'
    success_url = reverse_lazy('nucleo:indexCliente')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            cliente=form.save(commit=False)
            cliente.fechaAlta = datetime.today()
            cliente.activo = False
            cliente.is_cliente = True
            cliente.set_password(form.cleaned_data["password"])
            cliente.save()
            
        return redirect('nucleo:indexCliente')
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def verCliente(request):
    cliente=User.objects.filter(is_cliente=True)
    context={'cliente':cliente}
    return render(request, 'nucleo/Cliente/index.html',context)

@staff_member_required
def activarCliente(request, pk):
    cliente=User.objects.filter(is_cliente=True)
    context={'cliente':cliente}
    User.objects.filter(pk=pk).update(activo=1)
    return render(request, 'nucleo/Cliente/index.html',context)

@staff_member_required
def desactivarCliente(request,pk):
    cliente=User.objects.filter(is_cliente=True)
    context={'cliente':cliente}
    User.objects.filter(pk=pk).update(activo=0)
    return render(request, 'nucleo/Cliente/index.html', context)

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
    success_url = reverse_lazy('nucleo:indexCliente')
@staff_member_required
def borrarCliente(request,pk):
    cliente = User.objects.get(id=pk)
    cliente.delete()
    return redirect('nucleo:Clientes')
    
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


@empleadoTrue
def borrarProyecto(request,pk):
    proyecto = Proyectos.objects.get(id=pk)
    proyecto.delete()
    return redirect('nucleo:indexProyectos')
        
@method_decorator(noAdmin, name='dispatch')
class ProyectoFilter(ListView):
    model = Proyectos
    template_name = 'nucleo/Proyectos/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        idProj = []
        inscripciones = Participa.objects.filter(idCliente=self.request.user.id)
        
        categoria = self.request.GET.get('category', None)
        fechaIni = self.request.GET.get('fechaIni',None)
        fechaFin = self.request.GET.get('fechaFin',None)

        if categoria is not None and fechaIni != '' and fechaFin != '':
            projectos = Proyectos.objects.filter(idCategoria=categoria,fechafin=fechaFin).exclude(pk__in = idProj)
        elif fechaIni is None and fechaFin is None:
            projectos = Proyectos.objects.filter().exclude(pk__in = idProj)
        elif fechaIni != '' and fechaFin != '':
            projectos = Proyectos.objects.filter(fechafin=fechaFin).exclude(pk__in = idProj)
        elif categoria is not None and categoria != '0':
            projectos = Proyectos.objects.filter(idCategoria=categoria).exclude(pk__in = idProj)
        else:
            projectos = Proyectos.objects.filter().exclude(pk__in = idProj)

        context['proyectos'] = projectos
        context['categorias'] = Categorias.objects.all()
        
        return context
@noAdmin
def verProyectos(request):
    proyectos=Proyectos.objects.all()
    context={'proyectos':proyectos}
    
    return render(request, 'nucleo/Proyectos/index.html', context)

@clienteTrue
def ParticipaCreate(request,pk):
    AlredyIns = Participa.objects.filter(idProyecto_id=pk).filter(idCliente_id=request.user.id).exists()
    
    proyectos=Proyectos.objects.all()
    proyecto = Proyectos.objects.filter(pk=pk).first()
    user = User.objects.filter(pk=request.user.id).first()
    participa = Participa.objects.all()
    if (AlredyIns == True ):
        context={'proyectos':proyectos,
                'user':user,
                'participa': participa,
                'AI':AlredyIns}
       
        
        
        return render(request, 'nucleo/Proyectos/index.html', context)
    else:
        if proyecto is not None:
            
            inscripcion = Participa()
            inscripcion.idCliente = user
            inscripcion.idProyecto = proyecto
            inscripcion.fechaInscripcion = datetime.today()
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


@staff_member_required
def borrarCategoria(request,pk):
    categoria = get_object_or_404(Categorias, id=pk)
    
    categoria.foto.delete()
    categoria.delete()
    return redirect('nucleo:indexCategoria')

@staff_member_required
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
    
class proyectoSiguiente(ListView):
    model = Proyectos
    template_name = 'nucleo/Proyectos/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.today()
        week = date.strftime("%V")
        week = int(week) + 1
        # project = Project.objects.filter(initDateweek = week).order_by('-initDate')

        proyecto = Proyectos.objects.filter(fechaInicioweek = week).order_by('-fechaInicio')

        context['proyectos'] = proyecto
        context['categorias'] = Categorias.objects.all()
        
        return context
    
@empleadoTrue
def clienteProyecto(request,pk):
    inscritos=Participa.objects.filter(idProyecto=pk)
    proyecto=Proyectos.objects.get(id=pk)
    context={'inscritos':inscritos,
             'proyecto':proyecto}
    
    return render(request, 'nucleo/Proyectos/clienteProyecto.html', context)

@empleadoTrue
def asignarRol(request,pk):
    N=request.POST.get('rol')
    NUM=request.POST.get('proyectoid')
    
    ROLF=N.replace(" ","_")
    Participa.objects.filter(pk=pk).update(rol=ROLF)
    inscritos=Participa.objects.filter(idProyecto=NUM)
    proyecto=Proyectos.objects.get(id=NUM)
    context={'inscritos':inscritos,
             'proyecto':proyecto}
    
    return render(request, 'nucleo/Proyectos/clienteProyecto.html', context)
    
@empleadoTrue
def indexRolCliente(request):
    cliente=User.objects.filter(is_cliente=True)
    context={'cliente':cliente}
    return render(request, 'nucleo/Cliente/indexRol.html',context)
