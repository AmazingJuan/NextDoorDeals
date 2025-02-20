from django.shortcuts import render
from django.http import HttpResponse
from .models import Property
from .models import City
from .models import District
# Create your views here.
def filterPrice(minAttr, maxAttr, property):
    if minAttr:
        minAttr = float(minAttr)
        print(minAttr)
        property = property.filter(price__gte = minAttr)
    print(property)
    if maxAttr:
        maxAttr = float(maxAttr)
        if minAttr and minAttr <= maxAttr:
            property = property.filter(price__lte = maxAttr)
        elif not minAttr:
            property = property.filter(price__lte = maxAttr)
    return property

def filterSES(minAttr, maxAttr, property):
    if minAttr:
        minAttr = int(minAttr)
        property = property.filter(socioEconomicStatus__gte = minAttr)
    if maxAttr:
        maxAttr = int(maxAttr)
        if minAttr and minAttr <= maxAttr:
            property = property.filter(socioEconomicStatus__lte = maxAttr)
        elif not minAttr:
            property = property.filter(socioEconomicStatus__lte = maxAttr)
    return property

def filterDistrict(district, properties):
    return properties.filter(addressID__neigID__dID = district)
    

def home(request):
    searchTerm = request.GET.get('searchProperty')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    minSES = request.GET.get('minSES')
    maxSES = request.GET.get('maxSES')
    district = request.GET.get('district')
    print(minSES, maxSES)
    properties = Property.objects.all()
    properties = filterPrice(minPrice, maxPrice, properties)
    properties = filterSES(minSES, maxSES, properties)
    cities = City.objects.all()
    districts = District.objects.all()
    
    if searchTerm: 
        properties = properties.filter(name__icontains = searchTerm)
    else:
        searchTerm = None

    if district:
        properties = filterDistrict(district, properties)

    propertyPresence = True if properties.count() > 0 else False
    
    return render(request, 'home.html', {'searchTerm': searchTerm, 
        'propertys': properties, 'minPrice': minPrice, 'maxPrice': maxPrice, 
        'propertyPresence' : propertyPresence, 'districts': districts})
