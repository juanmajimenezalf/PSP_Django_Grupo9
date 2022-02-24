
from asyncio.windows_events import NULL
from enum import Flag
from fileinput import filename
import os
from re import I
import string
from tkinter import CURRENT, N
from urllib import response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import CreateView, UpdateView,DeleteView, ListView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from nucleo.serializers import ProyectosSerializers
from nucleo.decorators import clienteTrue, empleadoTrue, noAdmin
from datetime import datetime
from nucleo.forms import UserForm, EditUserForm, proyectosForm, ClienteForm, categoriasForm
from nucleo.models import User,Proyectos,Participa,Categorias
from django.contrib import messages

import io
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


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
        if(self.request.user.is_empleado):
            if categoria is not None and fechaIni != '' and fechaFin != '':
                projectos = Proyectos.objects.filter(idCategoria=categoria,fechafin=fechaFin, idEmpleado=self.request.user.id).exclude(pk__in = idProj)
            elif fechaIni is None and fechaFin is None:
                projectos = Proyectos.objects.filter(idEmpleado=self.request.user.id).exclude(pk__in = idProj)
            elif fechaIni != '' and fechaFin != '':
                projectos = Proyectos.objects.filter(fechafin=fechaFin,idEmpleado=self.request.user.id).exclude(pk__in = idProj)
            elif categoria is not None and categoria != '0':
                projectos = Proyectos.objects.filter(idCategoria=categoria,idEmpleado=self.request.user.id).exclude(pk__in = idProj)
            else:
                projectos = Proyectos.objects.filter(idEmpleado=self.request.user.id).exclude(pk__in = idProj)
        else:
            if categoria is not None and fechaIni != '' and fechaFin != '':
                projectos = Proyectos.objects.filter(idCategoria=categoria,fechafin=fechaFin).exclude(pk__in = idProj)
            elif fechaIni is None and fechaFin is None:
                projectos = Proyectos.objects.filter().exclude(pk__in = idProj)
            elif fechaIni != '' and fechaFin != '':
                projectos = Proyectos.objects.filter(fechafin=fechaFin,).exclude(pk__in = idProj)
            elif categoria is not None and categoria != '0':
                projectos = Proyectos.objects.filter(idCategoria=categoria,).exclude(pk__in = idProj)
            else:
                projectos = Proyectos.objects.filter().exclude(pk__in = idProj)
        context['proyectos'] = projectos
        context['categorias'] = Categorias.objects.all()
        
        return context
@noAdmin
def verProyectos(request):
    if(request.user.is_empleado):
        proyectos=Proyectos.objects.filter(idEmpleado=request.user.id)
    else:
        proyectos=Proyectos.objects.filter()
    categorias = Categorias.objects.all()
    context={'proyectos':proyectos, 'categorias':categorias}
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
            inscripcion.rol = 'Sin_rol'
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
    proyecto=Proyectos.objects.get(id=NUM, idEmpleado=request.user.id)
    context={'inscritos':inscritos,
             'proyecto':proyecto}
    
    return render(request, 'nucleo/Proyectos/clienteProyecto.html', context)

@empleadoTrue
def finalizarProyecto(request,pk):
    proyecto=Proyectos.objects.get(id=pk)
    context={'proyecto':proyecto}
    print(proyecto.idEmpleado)
    if(proyecto.idEmpleado != request.user or proyecto.informeFinal is not None):
        return redirect('nucleo:indexProyectos')
    return render(request, 'nucleo/Proyectos/finalizarProyecto.html', context)

@empleadoTrue
def actualizarInforme(request,pk):
    
    N=request.POST.get('informe')
  
    Proyectos.objects.filter(pk=pk).update(informeFinal=N)
    Proyectos.objects.filter(pk=pk).update(fechafin=datetime.today())
    return redirect('nucleo:indexProyectos')

@empleadoTrue
def indexRol(request):
    proyecto=Proyectos.objects.filter(idEmpleado=request.user.id)
    Data=Participa.objects.filter(idProyecto__in=proyecto)
    roles=Participa.objects.filter(idProyecto__in=proyecto).values_list('rol', flat=True).distinct()
    context={'roles':roles,'Data':Data}
    return render(request, 'nucleo/Cliente/indexRol.html', context) 

@method_decorator(empleadoTrue, name='dispatch')
class indexRolCliente(ListView):
    model = Participa
    template_name = 'nucleo/Cliente/indexRol.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto=Proyectos.objects.filter(idEmpleado=self.request.user.id)
        rolGet=self.request.GET.get('rol')
        roles=Participa.objects.filter(idProyecto__in=proyecto).values_list('rol', flat=True).distinct()

        if(self.request.GET.get('rol')!= '0'):
            
            Data=Participa.objects.filter(rol=rolGet,idProyecto__in=proyecto)
        else:
            
            Data=Participa.objects.filter(idProyecto__in=proyecto)

        context['roles'] = roles
        context['Data'] = Data
    
        
        return context
    
@clienteTrue
def pdfCliente(request):
    
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
   
    
    pdf = canvas.Canvas(buffer)
    user=User.objects.get(id=request.user.id)
    logo=os.path.join(os.getcwd(),'static/users/logo_salesianos.jpg')
    pdf.drawImage(logo, 25, 720, 120, 90,preserveAspectRatio=True)
    pdf.setFont("Helvetica-Bold", 21)
    Pa=2
    pdf.drawString(230, 790, u"GESTIÓN OFERTAS")
    pdf.setFont("Helvetica-Bold", 17)
    
    pdf.drawString(200, 750, u"LISTA DE PROYECTOS EN LOS")
    pdf.drawString(205, 730, u"QUE PARTICIPA EL USUARIO:")
    pdf.setFont("Helvetica-Oblique", 16)
    pdf.drawString(285, 700, user.nombre + user.apellidos)
    FI = request.GET.get('FIPDF')
    FF = request.GET.get('FFPDF')
    participa=Participa.objects.filter(idCliente=request.user.id).values_list('idProyecto', flat=True)
    proyectos=Proyectos.objects.filter(id__in=participa,fechainiciacion__range=(FI, FF) )
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(40, 640, u"Entre las fechas: " + FI +" y " +FF)
    
    pdf.drawString(540, 20, "1")
    Y=465
    style = getSampleStyleSheet()['Normal']
    def P(txt):
        return Paragraph(txt, style)
    F=0
    
    for p in proyectos:
       
        if(Y-180)<=200:
            print(Y)
            pdf.showPage()
            logo=os.path.join(os.getcwd(),'static/users/logo_salesianos.jpg')
            pdf.drawImage(logo, 40, 750, 20, 20,preserveAspectRatio=True)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(540, 20, str(Pa))
            Y=600
            F=0
            Pa=Pa+1
        elif F>0:
            Y=Y-200
        F=1
        foto = Image(str(p.idCategoria.foto), 3*cm, 3*cm)  
        datos = [('Titulo:',P(p.titulo),foto)]
        datos += [('Descripción:', P(p.descripcion))]
        datos += [('Nivel:', P(str(p.nivel)))]
        datos += [('Categoria:', P(p.idCategoria.nombre))]
       
        datosTable = Table(datos, colWidths=[6*cm])
       
        datosTable.setStyle(TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                
                ('FONTNAME', (0,0), (0,-1), 'Helvetica'),
                ('SPAN', (2, 0), (-1, -1)),
            ]
        ))
       
        datosTable.wrapOn(pdf, 800, 100)
        
        datosTable.drawOn(pdf, 40,Y)
    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

class LoginAPI(APIView):
    
    def get(self,request,format=None):
        return Response({'detail':'GET Response'})
    def post(self, request, format=None):
        try:
            data=request.data
        except ParseError as error:
            return Response(
                'INVALID JASON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Credenciales erroneas',
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.get(username=data["user"])
        
        if not user:
            return Response(
                'No usuario, crea uno',
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_cliente == False or user.activo==0 or check_password(data["password"],user.password)==False:
            return Response(
                'Usuario no autorizado',
                status=status.HTTP_404_NOT_FOUND
            )
        
        token = Token.objects.get_or_create(user=user)
        
        return Response({'token': token[0].key})

class Historial_APIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        participa=Participa.objects.filter(idCliente=request.user.id).values_list('idProyecto', flat=True)
        
        proyectos=Proyectos.objects.filter(id__in=participa,fechainiciacion__lt=datetime.today() )
        
        serializer= ProyectosSerializers(proyectos,many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ProyectosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
