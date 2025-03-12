from django import forms
from .utilities import getUserType
from .utilities import getRole


class AccountForm(forms.Form):
    
    username = forms.CharField(label = "Username: ", max_length = 16)
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)
    email = forms.EmailField(label = "Email: ")
    phone = forms.IntegerField(label = "Phone Number: ")
    
    userType = forms.ChoiceField(
        choices = getUserType(), 
        widget=forms.Select(attrs={'id': 'userType', 'class': 'form-control'}),  
    )

class NaturalForm(forms.Form):

    firstName = forms.CharField(label = "First Name: ")
    lastName = forms.CharField(label = "Last Name:  ")
    id = forms.IntegerField(label = "DNI: ")
    role = forms.ChoiceField(
        choices = getRole(), 
        widget=forms.Select(attrs={'class': 'form-control'})  
    )