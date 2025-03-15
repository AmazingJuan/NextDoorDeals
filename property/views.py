from django.shortcuts import render
from .models import Property, City, District, Images, PropertyType
from .forms import PublishForm
from django.contrib import messages
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

def filterSES(minAttr, maxAttr, property, isChecked, attr):
    if isChecked and attr:
        attr = int(attr)
        property = property.filter(socioEconomicStatus__exact=attr)
    else:
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

    # Capturar valores faltantes para filtro SES
    isChecked = request.GET.get('useRangeSES', 'off') == 'on'  # Verifica si el checkbox está marcado
    attr = request.GET.get('singleSES', None)  # Estrato único si el checkbox está activado

    print(minSES, maxSES, isChecked, attr)  # Para depuración

    properties = Property.objects.all()
    properties = filterPrice(minPrice, maxPrice, properties)
    properties = filterSES(minSES, maxSES, properties, isChecked, attr)  # Ahora los parámetros están definidos
    cities = City.objects.all()
    districts = District.objects.all()

    if searchTerm: 
        properties = properties.filter(name__icontains=searchTerm)
    else:
        searchTerm = None

    if district:
        properties = filterDistrict(district, properties)

    propertyPresence = properties.exists()  # Mejor alternativa a count() > 0

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'propertys': properties,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
        'propertyPresence': propertyPresence,
        'districts': districts
    })


def publish(request):
    if request.method == "POST":
        publishForm = PublishForm(request.POST, request.FILES)
        if publishForm.is_valid():
            data = publishForm.cleaned_data
            title = data["title"]
            type = data["type"]
            description = data["description"]
            SES = data["SES"]
            price = data["price"]
            newProperty = Property(title = title, description = description, SES = SES, price = price, propertyType = PropertyType.objects.get(id = int(type)-1))
            newProperty.save()
            images = data["pictures"]
            for i in images:
                Images.objects.create(property = newProperty, image = i)
            publishForm = PublishForm()
            messages.success(request, "Property published succesfully")
    else:
        publishForm = PublishForm()
    return render(request, 'publish.html', {'publishForm':publishForm})
