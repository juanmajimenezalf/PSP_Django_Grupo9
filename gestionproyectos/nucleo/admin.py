from django.contrib import admin

from .models import User,Proyectos,Categorias, Participa

# Register your models here.
admin.site.register(User)
admin.site.register(Proyectos)
admin.site.register(Categorias)
admin.site.register(Participa)