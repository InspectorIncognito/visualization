from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'login.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        print("hola")