from django.shortcuts import render
from .models import Account, UserType
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import AccountForm, NaturalForm, BussinesForm
from .utilities import getRole
from .models import Account, BussinessAccount, PersonAccount, UserType, Role
# Create your views here.


def signupSuccess(request):
     
     return render("signUp/")

def createUser(request):
        regularForm = AccountForm(request.POST)
        regularForm.is_valid()
        regularForm = regularForm.cleaned_data
        print(regularForm.values())
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
    print(request.path)
    if request.method == "POST":
        return createUser(request)
    else:
        naturalForm = NaturalForm()
        accountForm = AccountForm()
        bussinesForm = BussinesForm()
        return render(request, 'signup.html', {"userType": accountForm, "naturalForm" : naturalForm, "roles": getRole(), "requestPath":request.path, "bussinesForm":bussinesForm})
    

         
        
        
    


