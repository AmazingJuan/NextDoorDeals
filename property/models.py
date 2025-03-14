from django.db import models

# Create your models here.

class Cardinality(models.Model):
    name = models.CharField(max_length=10)

class RoadType(models.Model):
    name = models.CharField(max_length=20)

class Province(models.Model):
    name = models.CharField(max_length = 50)
    
class City(models.Model):
    provinID = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    
class District(models.Model):
    name = models.CharField(max_length = 50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    dID = models.ForeignKey(District, on_delete=models.CASCADE)
    
class Address(models.Model):
    roadType = models.ForeignKey(RoadType, on_delete=models.CASCADE)
    road = models.IntegerField()
    roadPrefix = models.CharField(max_length=10, null=True, blank=True)
    crossingPrefix = models.CharField(max_length=10, null=True, blank=True)
    roadCardinality = models.ForeignKey(Cardinality, on_delete=models.CASCADE, null = True, blank=True)
    crossingCardinality = models.CharField(max_length=10, null=True, blank=True)
    plateNumber = models.CharField(max_length=10)
    neigID = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)

class PropertyType(models.Model):
    name = models.CharField(max_length = 50)

class Property(models.Model):
    title = models.CharField(max_length = 50)   
    description = models.CharField(max_length = 1000) 
    propertyType = models.ForeignKey(PropertyType, on_delete = models.CASCADE)
    price = models.IntegerField()
    SES = models.CharField(max_length = 1)
    addressID = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(null = True, blank = True, upload_to= "property/images")

