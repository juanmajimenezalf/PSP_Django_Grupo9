from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from registration.forms import EditUserProfileForm

from registration.forms import UserCreationFormEmail


# Create your views here.

class Login(LoginView):
    template_name = 'login.html'


class SignupView(CreateView):
    form_class=UserCreationFormEmail
    template_name='registration/register.html'

    def get_succes_url(self):
        return reverse_lazy('login')+'?register'

    def get_form(self, form_class=None):
        form=super(SignupView,self).get_form()
        form.yields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
        'placeholder':'Nombre de usuario'})
        form.yields['email'].widget=forms.EmailInput(attrs={'class':'form-control mb2',
        'placeholder':'Mail'})
        form.yields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Contraseña'})
        form.yields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Repite la contraseña'})
        return form
class UserEditView(UpdateView):
    form_class = EditUserProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('nucleo:home')

    def get_object(self):
        return self.request.user