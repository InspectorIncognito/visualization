from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from .models import LoginForm
from carrier.views import index as cindex
from django.template import loader

def login(request):
    """ check if user is logged in system """
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect(cindex)
    if request.POST and form.is_valid():
        user = form.login(cindex)
        if user:
            auth_login(request, user)
            return redirect(cindex)
    template = loader.get_template('login.html')
    context = {"form" : form}
    return HttpResponse(template.render(context, request))

def logout(request):
    auth_logout(request)
    return redirect(login)
