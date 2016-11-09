from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from carrier.views import index as cindex

def index(request):
    if request.user.is_authenticated():
        return redirect(login)
    return render(request, 'login.html')

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
