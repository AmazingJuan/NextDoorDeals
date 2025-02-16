from django.shortcuts import render
from django.http import HttpResponse
from .models import Property

# Create your views here.

def home(request):

    searchTerm = request.GET.get('searchProperty')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    property = Property.objects.all()
    print(property)
    if minPrice:
        minPrice = float(minPrice)
        property = property.filter(price__gte = minPrice)
    if maxPrice:
        maxPrice = float(maxPrice)
        if minPrice and minPrice <= maxPrice:
            property = property.filter(price__lte = maxPrice)
        elif not minPrice:
            property = property.filter(price__lte = maxPrice)


    if searchTerm: 
        property = property.filter(name__icontains = searchTerm)
    else:
        searchTerm = None

    propertyPresence = True if property.count() > 0 else False
    
    return render(request, 'home.html', {'searchTerm': searchTerm, 'propertys': property, 'minPrice': minPrice, 'maxPrice': maxPrice, 'propertyPresence' : propertyPresence})
 

   