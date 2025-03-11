from django.db import models

# Create your models here.
class UserType(models.Model): 

    idUserType = models.IntegerField(blank = False, primary_key=True)
    nameUserType = models.CharField(blank = False, max_length= 30)


class Account(models.Model):

    username = models.CharField(blank= False, max_length= 11)
    password = models.CharField(blank= False, max_length= 70)
    profilePicture = models.ImageField()
    cellphone = models.IntegerField()
    email = models.CharField(blank = False, max_length= 50)
    idAccount = models.IntegerField(blank = False, primary_key=True) 
    userType = models.ForeignKey(UserType, on_delete = models.CASCADE)
    #registrationTime = models.TimeField() ????

    #def __str__(self): return self.username 

class Role(models.Model):

    idRole = models.IntegerField(blank = False, primary_key=True)
    nameRole = models.CharField(blank = False, max_length= 20)

class PersonAccount(models.Model):

    firstName = models.CharField(max_length= 30)
    lastName = models.CharField(max_length= 30)
    idPersonAccount = models.IntegerField(blank = False, primary_key=True)
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    #aquí todos los atributos de la person account

class BussinessAccount(models.Model): 

    nitBussinessAccount = models.IntegerField(blank = True, primary_key=True)
    nameBussiness = models.CharField(max_length= 20)
    roleBussinessAccount = models.ForeignKey(Role, on_delete = models.CASCADE)

    #aquí todos los atributos de la bussiness account


