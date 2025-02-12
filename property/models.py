from django.db import models

# Create your models here.

class Property(models.Model):

    name = models.CharField(max_length= 50)   
    description = models.CharField(max_length= 300) 
    propertyType = models.CharField(max_length= 20)
    price = models.FloatField()
    location = models.URLField()
    socioEconomicStatus = models.CharField(max_length= 1)
    ID = models.FloatField()


