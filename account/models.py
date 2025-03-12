from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserType(models.Model): 

    idUserType = models.IntegerField(blank = False, primary_key=True)
    nameUserType = models.CharField(blank = False, max_length= 30)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE)
    profilePicture = models.ImageField(null = True)
    phone = models.IntegerField()
    userType = models.ForeignKey(UserType, on_delete = models.CASCADE)
    #registrationTime = models.TimeField() ????

    #def __str__(self): return self.username 

class Role(models.Model):

    idRole = models.IntegerField(blank = False, primary_key=True)
    nameRole = models.CharField(blank = False, max_length= 20)

class PersonAccount(models.Model):

    firstName = models.CharField(max_length= 30)
    lastName = models.CharField(max_length= 30)
    id = models.OneToOneField(Account, on_delete = models.CASCADE, blank = False, primary_key=True)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    #aquí todos los atributos de la person account

class BussinessAccount(models.Model): 
    id = models.OneToOneField(Account, on_delete = models.CASCADE, blank = False, primary_key=True)
    nitBussinessAccount = models.IntegerField(blank = True)
    nameBussiness = models.CharField(max_length= 20)
    roleBussinessAccount = models.ForeignKey(Role, on_delete = models.CASCADE)

    #aquí todos los atributos de la bussiness account


