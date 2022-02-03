from django.contrib import admin

from .models import User,proyectos,categorias

# Register your models here.
admin.site.register(User)
admin.site.register(proyectos)
admin.site.register(categorias)