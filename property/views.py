from django.shortcuts import render
from django.http import HttpResponse
from .models import Property

# Create your views here.

def home(request):

    searchTerm = request.GET.get('searchProperty')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')

    if searchTerm: 
        property = Property.objects.filter(name__icontains = searchTerm)
    else:
        property = Property.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'propertys': property, 'minPrice': minPrice, 'maxPrice': maxPrice})
 

   