from django import forms
from .utilities import getUserType
from .utilities import getRole

class AccountForm(forms.Form):
    username = forms.CharField(label = "Username: ", max_length = 16)
    password = forms.CharField(label = "Password: ", widget = forms.PasswordInput)
    email = forms.EmailField(label = "Email: ")
    phone = forms.IntegerField(label = "Phone Number: ")
    userType = forms.ChoiceField(
        choices = getUserType(), 
        widget=forms.Select(attrs={'id': 'userType'}),  
    )
    role = forms.ChoiceField(
        choices = getRole(), 
        widget=forms.Select(attrs={'class': 'form-control'}), required=False  
    ) 

class NaturalForm(forms.Form):
    firstName = forms.CharField(label = "First Name: ", required=False)
    lastName = forms.CharField(label = "Last Name:  ", required=False)

class BussinesForm(forms.Form):
    nit = forms.IntegerField(label = "NIT: ", required=False)
    name = forms.CharField(label = "Bussines Name:  ", required=False)

class loginForm(forms.Form):
    username = forms.CharField(label = "Username: ")
    password = forms.CharField(label = "Password: ", widget = forms.PasswordInput)
