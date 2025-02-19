from django.db import models

# Create your models here.

class Province(models.Model):
    
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    
class City(models.Model):
    
    id = models.IntegerField(primary_key = True)
    provinID = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    
class District(models.Model):
    
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
class Neighborhood(models.Model):
    
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=50)
    dID = models.ForeignKey(District, on_delete=models.CASCADE)
    
class Address(models.Model):
    
    roadType = models.CharField(max_length=50)
    road = models.IntegerField()
    roadPrefix = models.CharField(max_length=10, null=True, blank=True)
    crossingPrefix = models.CharField(max_length=10, null=True, blank=True)
    roadCardinality = models.CharField(max_length=10, null=True, blank=True)
    crossingCardinality = models.CharField(max_length=10, null=True, blank=True)
    plateNumber = models.CharField(max_length=10)
    neigID = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    
class Property(models.Model):
    
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)   
    description = models.CharField(max_length = 1000) 
    image = models.ImageField(upload_to = 'property/images', null = True)
    propertyType = models.CharField(max_length = 20)
    price = models.FloatField()
    location = models.URLField()
    socioEconomicStatus = models.CharField(max_length = 1)
    #address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)