from django.shortcuts import render
from .models import Account
from django.http import HttpResponse

# Create your views here.

def account(request): 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profilePicture')
        return HttpResponse(f"Usuario registrado: {username}, Foto: {profile_picture}")
    return render(request, 'account.html')
    #return render(request, 'account.html')
