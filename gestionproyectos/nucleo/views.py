from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView

class SingupView(CreateView):
    form_class=UserCreationForm
    template_name='registration/registro.html'
    
    def get_succes_url(self):
        return reverse_lazy('login')+'?register'

    def get_form(self, form_class=None):
        form=super(SingupView,self).get_form()
        form.yields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
        'placeholder':'Nombre de usuario'})
        form.yields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Contraseña'})
        form.yields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Repite la contraseña'})
        return form
