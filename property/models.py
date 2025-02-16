from django.db import models

# Create your models here.

class Property(models.Model):

    name = models.CharField(max_length= 50)   
    description = models.CharField(max_length= 1000) 
    image = models.ImageField(upload_to= 'property/images', null = True)
    propertyType = models.CharField(max_length= 20)
    price = models.FloatField()
    location = models.URLField()
    socioEconomicStatus = models.CharField(max_length= 1)
    identificator = models.FloatField(null = True)
    #district = models.IntegerField(null = True)


