from django.contrib import admin

from .models import User,Proyectos,Categorias

# Register your models here.
admin.site.register(User)
admin.site.register(Proyectos)
admin.site.register(Categorias)