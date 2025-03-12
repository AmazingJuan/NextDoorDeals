from django.shortcuts import render
from .models import Account
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here.


def create_user(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username = username, password = password, email = email)
        login(request, user)
        return redirect('url de tin')




def signup(request): 
    if request.method == "POST":
        create_user(request)
    else:
        return render(request, 'signup.html')
    #return render(request, 'account.html')


