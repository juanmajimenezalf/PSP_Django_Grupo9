"""gestionproyectos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from nucleo.views import proyectoCreate, proyectoUpdate, proyectoDelete, categoriaCreate, categoriaUpdate, categoriaDelete
from nucleo import views
from nucleo.decorators import clienteTrue, empleadoTrue

app_name = "nucleo"
urlpatterns = [
    
    path('home', views.home, name= "home"),
    
    path('empleados', views.verEmpleados, name="indexEmpleado"),
    path('empleados/create', views.empleadoCreate.as_view(), name="crearEmpleado"),
    path('empleados/update/<int:pk>', views.EmpleadoUpdate.as_view(), name="editarEmpleado"),
    path('empleados/delete/<int:pk>', views.EmpleadoDelete.as_view(), name="borrarEmpleado"),    
    
    path('Clientes', views.verCliente, name="indexCliente"),
    path('Clientes/activate/<int:pk>', views.activateCliente, name="activarCliente"),
    path('Clientes/create', views.clienteCreate.as_view(), name="crearCliente"),
    path('Clientes/update/<int:pk>', views.ClienteUpdate.as_view(), name="editarCliente"),
    path('Clientes/delete/<int:pk>', views.ClienteDelete.as_view(), name="borrarCliente"),
    
    path('proyectos', views.verProyectos, name="indexProyectos"),
    path('proyectos/create', views.proyectoCreate.as_view(), name="crearProyecto"),
    path('proyectos/update/<int:pk>', views.proyectoUpdate.as_view(), name="editarProyecto"),
    path('proyectos/delete/<int:pk>', views.proyectoDelete.as_view(), name="borrarProyecto"),
    
    path('Participa/create/<int:pk>', views.ParticipaCreate, name="crearParticipa"),
    
    path('categorias/create', views.categoriaCreate.as_view(), name="crearCategoria"),
    path('categorias/update/<int:pk>', views.categoriaUpdate.as_view(), name="editarCategoria"),
    path('categorias/delete/<int:pk>', views.categoriaDelete.as_view(), name="borrarCategoria"),
    path('categorias', views.verCategorias, name="indexCategoria"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
