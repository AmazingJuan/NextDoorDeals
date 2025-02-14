from django.shortcuts import render
from django.http import HttpResponse
from .models import Property

# Create your views here.

def home(request):
    #return render(request, 'home.html')
    searchTerm = request.GET.get('searchProperty')
    if searchTerm: 
        property = Property.objects.filter(name__icontains = searchTerm)
    else:
        property = Property.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'propertys': property})
   