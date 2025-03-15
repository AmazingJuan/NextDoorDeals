from django.shortcuts import render, redirect
from .models import Account, UserType
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import AccountForm, NaturalForm, BussinesForm, loginForm
from .utilities import getRole
from .models import Account, BussinessAccount, PersonAccount, UserType, Role
from django.contrib import messages
# Create your views here.


def signupSuccess(request):
     
     return render(request, 'success.html')

def createUser(request):
        regularForm = AccountForm(request.POST)
        regularForm.is_valid()
        regularForm = regularForm.cleaned_data
        personForm = NaturalForm(request.POST)
        personForm.is_valid()
        personForm = personForm.cleaned_data
        user = User.objects.create_user(username = regularForm["username"], password = regularForm["password"], email = regularForm["email"])
        if(regularForm["userType"] == 'persona'):
            userType = 1
        else:
            userType = 2
        cuenta = Account(user = user, phone = regularForm["phone"], userType = UserType.objects.get(idUserType=userType))
        cuenta.save()

        role = int(personForm["role"]) - 1
        if(regularForm["userType"] == 'persona'):

            persona = PersonAccount(associatedAccount = cuenta, firstName = personForm["firstName"], lastName = personForm["lastName"], role = Role.objects.get(idRole = role) )
            persona.save()
        else:
            userType = 2
        login(request, user)
        return redirect('SUsuccess')




def signup(request): 
    if request.method == "POST":
        return createUser(request)
    else:
        naturalForm = NaturalForm()
        accountForm = AccountForm()
        bussinesForm = BussinesForm()
        return render(request, 'signup.html', {"userType": accountForm, "naturalForm" : naturalForm, "roles": getRole(), "requestPath":request.path, "bussinesForm":bussinesForm})


def loginUser(request): 
     
    if request.method == "POST":
            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')  # Cambia 'home' por la URL de la página de inicio
                else:
                    messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = loginForm()
        form.label_suffix = "" 
    return render(request, 'login.html', {'loginForm':form})

         
        
        
    


