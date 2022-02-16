from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

from nucleo.models import User


def clienteTrue(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def same_user(func):
    def check_and_call(request, *args, kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)

        if not request.user.is_staff:
            if not (user.id == request.user.id):
                
                if request.user.is_cliente == True:
                    return HttpResponseRedirect('/')
                elif request.user.is_empleado == True:
                    return HttpResponseRedirect('/')

        return func(request, *args, kwargs)

    return check_and_call

def empleadoTrue(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_empleado,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def noAdmin(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
       
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_cliente or u.is_active and u.is_empleado,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

