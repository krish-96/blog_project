from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.http import HttpResponse

def unauthenticated_user(func_auth):
    def wrapper_function(request, *args, **kwargs):
       if request.user.is_authenticated:
           return redirect('blog:dashboard')
       else:
           return func_auth(request, *args, **kwargs)

    return wrapper_function


