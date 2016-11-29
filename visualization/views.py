from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from carrier.views import index as cindex
from django.template import loader

def index(request):
    context = {}
    if request.user.is_authenticated():
        return redirect(login)
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))

def login(request):
    if request.user.is_authenticated():
        return redirect(cindex)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(cindex)
        else:
            return redirect(index)

def logout(request):
    auth_logout(request)
    return redirect(index)
