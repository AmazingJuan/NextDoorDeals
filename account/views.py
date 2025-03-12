from django.shortcuts import render
from .models import Account, UserType
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import AccountForm, NaturalForm

# Create your views here.


def createUser(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username = username, password = password, email = email)
        login(request, user)
        return redirect('url de tin')




def signup(request): 
    if request.method == "POST":
        createUser(request)
    else:
        naturalForm = NaturalForm()
        form = AccountForm()
        return render(request, 'signup.html', {"userType": form, "naturalForm" : naturalForm })
    


         
        
        
    


