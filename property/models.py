from django.db import models
from account.models import Account


    
class City(models.Model):
    name = models.CharField(max_length = 50)
    
class District(models.Model):
    name = models.CharField(max_length = 50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
class PropertyType(models.Model):
    name = models.CharField(max_length = 50)

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Location(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)

class Property(models.Model):
    title = models.CharField(max_length = 50)   
    description = models.CharField(max_length = 1000) 
    propertyType = models.ForeignKey(PropertyType, on_delete = models.CASCADE)
    price = models.IntegerField()
    SES = models.CharField(max_length = 1)
    associatedAccount = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='propertys')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)

class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="imagenes")
    image = models.ImageField(null = True, blank = True, upload_to= "property/images/")

class Favourites(models.Model):
    associatedAccount = models.ForeignKey(Account, on_delete = models.CASCADE, related_name= 'favouriteAccs')
    property = models.ForeignKey(Property, on_delete = models.CASCADE)
    class Meta:
        unique_together = ('associatedAccount', 'property') 

class AppointmentStatus(models.Model):
    name = models.CharField(max_length=30, blank = False, null = False)

class Appointment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name = 'appointments')
    requester = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.ForeignKey(AppointmentStatus, on_delete = models.CASCADE, default=3)

class Visit(models.Model):
    visited_user = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='visits')
    date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    reviewed_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    comment = models.CharField(max_length=280, blank=True, null=True)
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


