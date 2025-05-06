from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, City, District, Images, PropertyType, Favourites, Location, Coordinates, Visit, Review, Appointment, AppointmentStatus
from .forms import PublishForm, DateForm, EditPropertyForm
from account.views import checkSession
from django.contrib import messages
import os
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

def filterSES(minAttr, maxAttr, property):
    if minAttr:
        minAttr = int(minAttr)
        property = property.filter(SES__gte = minAttr)

    if maxAttr:
        maxAttr = int(maxAttr)
        if minAttr and minAttr <= maxAttr:
            property = property.filter(SES__lte = maxAttr)
        elif not minAttr:
            property = property.filter(SES__lte = maxAttr)
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
        publishForm = PublishForm(request.POST, request.FILES)
        if publishForm.is_valid():
            data = publishForm.cleaned_data
            title = data["title"]
            type = data["type"]
            description = data["description"]
            SES = data["SES"]
            district = data["district"]
            location = data["location"]
            coordinates = Coordinates.objects.create(latitude = location.y, longitude = location.x)
            location = Location(district = District.objects.get(id = int(district) - 1), coordinates = coordinates)
            location.save()
            price = data["price"]
            newProperty = Property(associatedAccount = request.user.account, title = title, description = description, SES = SES, price = price, propertyType = PropertyType.objects.get(id = int(type)-1), location = location)
            newProperty.save()
            images = data["pictures"]
            for i in images:
                Images.objects.create(property = newProperty, image = i)
            
            publishForm = PublishForm()
            messages.success(request, "Property published succesfully")
    else:
        publishForm = PublishForm()
    return render(request, 'publish.html', {'publishForm':publishForm, 'sessionActive':checkSession(request.user)})

def get_disabled_dates(property):
    appointments = property.appointments.filter(status__name = 'Approved')
    disabled_dates = []
    for appointment in appointments:
        disabled_dates.append(appointment.date)
    if len(disabled_dates) > 0:
        return disabled_dates
    else:
        return None

def request_appointment(property, date, account):
    Appointment.objects.create(property = property, requester = account, date = date)



def view_property(request, id):
    property = Property.objects.get(id = id)
    type = property.propertyType.name
    sessionActive = checkSession(request.user)
    if sessionActive and request.user != property.associatedAccount:
        disabled_dates = get_disabled_dates(property)
        needs_date_form = True
    else:
        disabled_dates = None
        needs_date_form = False
    
    if needs_date_form:
        date_form = DateForm(disabled_dates=disabled_dates)
    else:
        date_form = None

    Visit.objects.create(visited_user = property.associatedAccount)

    if sessionActive:
        is_fav = len(Favourites.objects.filter(property = property, associatedAccount = request.user.account)) != 0
    else:
        is_fav = None


    if request.POST:
        action = request.POST.get('action')
        if action == 'favourite':
            favourite(request, id)
        elif action == 'review':
            add_review(request, id)
        elif len(Appointment.objects.filter(property = property, date = request.POST.get('date'))) == 0:
            request_appointment(property, request.POST.get('date'), request.user.account)
        return redirect('property_info', id = id)
    else:
        return render(request, 'property_info.html', {'property':property, 'pType': type, 'is_fav': is_fav, 'sessionActive':sessionActive, 'date_form':date_form, 'api_key':os.getenv('maps_api')})
    try:
        ...
    except:
        return redirect('error')


#EDITAR LA PROPERTY 
def editProperty(request, id):
    property = Property.objects.get(id=id)
    sessionActive = checkSession(request.user)

    # Verificamos que la sesión esté activa y que el usuario sea el dueño
    if sessionActive and request.user != property.associatedAccount:

        if request.method == 'POST':
            form = EditPropertyForm(request.POST, request.FILES)
            if form.is_valid():
                # Actualizamos los campos de la propiedad
                property.title = form.cleaned_data['title']
                property.description = form.cleaned_data['description']
                property.propertyType = PropertyType.objects.get(id=form.cleaned_data['propertyType'])
                property.SES = form.cleaned_data['SES']
                property.price = form.cleaned_data['price']

                # Se actualiza la localización si es necesario
                district = District.objects.get(id=form.cleaned_data['location'])
                location = property.location
                location.district = district
                location.save()

                property.save()

                # Guardar las nuevas imágenes si se suben
                for image in form.cleaned_data['image']:
                    Images.objects.create(property=property, image=image)

                return redirect('property_info', id=property.id)  # o donde muestres la propiedad
        else:
            # Cargar datos iniciales del formulario
            initial_data = {
                'title': property.title,
                'description': property.description,
                'propertyType': property.propertyType.id,
                'SES': property.SES,
                'location': property.location.district.id,
                'price': property.price,
            }
            form = EditPropertyForm(initial=initial_data)
    else:
        print("No puedes editar esto bro")
        return redirect('home')  # o alguna otra vista a la que quieras redirigir

    context = {
        'form': form,
        'property': property,
    }

    return render(request, 'editProperty.html', context)


def favourite(request, id):
    account = request.user.account
    property = Property.objects.get(id = id)
    try:
        favourites = Favourites.objects.get(associatedAccount = account, property = property)
        favourites.delete()
    except:
        Favourites.objects.create(associatedAccount = account, property = property)
        
    
    return redirect('property_info', id = id)

def schedule_appointment(request, id):
    ...

def error(request):
    return render(request, 'error.html')

def add_review(request, id):
    account = request.user.account
    property = Property.objects.get(id = id)
    if request.POST:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(reviewer = account, reviewed_property = property, comment = comment, rating = rating )
    return redirect('property_info', id = id)