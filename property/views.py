from django.shortcuts import render, redirect
from .models import Property, City, District, Images, PropertyType, Favourites
from .forms import PublishForm
from django.contrib import messages
# Create your views here.



def filterPrice(minAttr, maxAttr, property):
    if minAttr:
        minAttr = float(minAttr)
        property = property.filter(price__gte = minAttr)
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

    isChecked = request.GET.get('useRangeSES', 'off') == 'on'  
    attr = request.GET.get('singleSES', None) 
    properties = Property.objects.all()
    properties = filterPrice(minPrice, maxPrice, properties)
    properties = filterSES(minSES, maxSES, properties, isChecked, attr) 
    cities = City.objects.all()
    districts = District.objects.all()

    if searchTerm: 
        properties = properties.filter(title__icontains=searchTerm)
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
        'districts': districts, 'types': PropertyType.objects.all()
    })


def publish(request):
    if request.method == "POST":
        print("aca")
        publishForm = PublishForm(request.POST, request.FILES)
        print(publishForm, publishForm.is_valid())
        if publishForm.is_valid():
            data = publishForm.cleaned_data
            title = data["title"]
            type = data["type"]
            description = data["description"]
            SES = data["SES"]
            price = data["price"]
            newProperty = Property(associatedAccount = request.user.account, title = title, description = description, SES = SES, price = price, propertyType = PropertyType.objects.get(id = int(type)-1))
            newProperty.save()
            images = data["pictures"]
            for i in images:
                Images.objects.create(property = newProperty, image = i)
            
            publishForm = PublishForm()
            print("aca")
            messages.success(request, "Property published succesfully")
        else:
            print(publishForm.errors)
    else:
        publishForm = PublishForm()
    return render(request, 'publish.html', {'publishForm':publishForm})

def view_property(request, id):
    property = Property.objects.get(id = id)
    type = property.propertyType.name

    if request.user.is_authenticated:
        is_fav = len(Favourites.objects.filter(property = property, associatedAccount = request.user.account)) != 0
    else:
        is_fav = None
    return render(request, 'property_info.html', {'property':property, 'pType': type, 'is_fav': is_fav })

def favourite(request, id):
    if request.user.is_authenticated:
        account = request.user.account
        property = Property.objects.get(id = id)
        favourites = Favourites.objects.filter(associatedAccount = account, property = property)
        if len(favourites) == 1:
            objects = favourites[0]
            objects.delete()
            print("delete")
        else:
            Favourites.objects.create(associatedAccount = account, property = property)
            print("create")
    
    return redirect('property_info', id = id)

def schedule_appointment(request, id):
    ...