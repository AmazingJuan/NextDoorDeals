from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserType(models.Model): 
    idUserType = models.IntegerField(blank = False, primary_key=True)
    nameUserType = models.CharField(blank = False, max_length= 30)

class Role(models.Model):
    idRole = models.IntegerField(blank = False, primary_key=True)
    nameRole = models.CharField(blank = False, max_length= 20)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE, primary_key= True, related_name='account')
    profilePicture = models.ImageField(null = True, blank = True)
    phone = models.IntegerField()
    userType = models.ForeignKey(UserType, on_delete = models.CASCADE)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)

class PersonAccount(models.Model):
    associatedAccount = models.OneToOneField(Account, on_delete = models.CASCADE, blank = False, primary_key=True)
    firstName = models.CharField(max_length= 30)
    lastName = models.CharField(max_length= 30)

    #aquí todos los atributos de la person account

class BussinessAccount(models.Model): 
    associatedAccount = models.OneToOneField(Account, on_delete = models.CASCADE, blank = False, primary_key=True)
    nitBussinessAccount = models.IntegerField(blank = True)
    nameBussiness = models.CharField(max_length= 20)

    #aquí todos los atributos de la bussiness account


