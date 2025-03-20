from django.shortcuts import render, redirect
from .models import Property, City, District, Images, PropertyType, Favourites, Location, Coordinates
from .forms import PublishForm
from account.views import checkSession
from django.contrib import messages
# Create your views here.

def filterPrice(minAttr, maxAttr, property):
    print(minAttr)
    if minAttr:
        print("im here")
        minAttr = float(minAttr)
        property = property.filter(price__gte = minAttr)
    if maxAttr:
        maxAttr = float(maxAttr)
        print(maxAttr)
        if minAttr and minAttr <= maxAttr:
            property = property.filter(price__lte = maxAttr)
        elif not minAttr:
            print("im here23")
            property = property.filter(price__lte = maxAttr)
    print(property)
    return property

def filterSES(minAttr, maxAttr, property):
    print(minAttr)
    print(maxAttr)
    if minAttr:
        minAttr = int(minAttr)
        property = property.filter(SES__gte = minAttr)

    if maxAttr:
        maxAttr = int(maxAttr)
        if minAttr and minAttr <= maxAttr:
            property = property.filter(SES__lte = maxAttr)
        elif not minAttr:
            property = property.filter(SES__lte = maxAttr)
        print(property)
    return property

def filterDistrict(district, properties):
    return properties.filter(location__district = district)
    

def home(request):
    searchTerm = request.GET.get('searchProperty')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    minSES = request.GET.get('minSES')
    maxSES = request.GET.get('maxSES')
    district = request.GET.get('district')

    isChecked = request.GET.get('useRangeSES') == 'on'  
    singleSES = request.GET.get('singleSES') 
    properties = Property.objects.all()
    properties = filterPrice(minPrice, maxPrice, properties)
    if not isChecked:
        print("aca aca")
        minSES = singleSES
        maxSES = singleSES
    properties = filterSES(minSES, maxSES, properties) 
    cities = City.objects.all()
    districts = District.objects.all()

    if searchTerm: 
        properties = properties.filter(title__icontains=searchTerm)
    else:
        searchTerm = None

    if district:
        properties = filterDistrict(district, properties)

    sessionActive = checkSession(request.user)

    print(request.GET.get("favourite"))
    if sessionActive and request.GET.get("favourite"):  # Si el usuario está autenticado y activó el filtro
        account = request.user.account
        favourite_properties = Favourites.objects.filter(associatedAccount=account).values_list('property', flat=True)
        properties = properties.filter(id__in=favourite_properties)  # Filtra solo las propiedades favoritas
    propertyPresence = properties.exists()

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'propertys': properties,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
        'propertyPresence': propertyPresence,
        'districts': districts, 'types': PropertyType.objects.all(),
        'sessionActive': sessionActive,
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
            district = data["district"]
            print("acacacaca", district)
            coordinates = Coordinates.objects.get(id = 1)
            print(coordinates)
            location = Location(district = District.objects.get(id = int(district) - 1), coordinates = coordinates)
            location.save()
            price = data["price"]
            newProperty = Property(associatedAccount = request.user.account, title = title, description = description, SES = SES, price = price, propertyType = PropertyType.objects.get(id = int(type)-1), location = location)
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
    return render(request, 'publish.html', {'publishForm':publishForm, 'sessionActive':checkSession(request.user)})

def view_property(request, id):
    property = Property.objects.get(id = id)
    type = property.propertyType.name
    sessionActive = checkSession(request.user)
    if sessionActive:
        is_fav = len(Favourites.objects.filter(property = property, associatedAccount = request.user.account)) != 0
    else:
        is_fav = None
    return render(request, 'property_info.html', {'property':property, 'pType': type, 'is_fav': is_fav, 'sessionActive':sessionActive})

def favourite(request, id):
    account = request.user.account
    property = Property.objects.get(id = id)
    favourites = Favourites.objects.filter(associatedAccount = account, property = property)
    if len(favourites) == 1:
        objects = favourites[0]
        objects.delete()
    else:
        Favourites.objects.create(associatedAccount = account, property = property)
    
    return redirect('property_info', id = id)

def schedule_appointment(request, id):
    ...