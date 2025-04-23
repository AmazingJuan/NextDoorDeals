from django import forms
from .utilities import getUserType
from .utilities import getRole
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

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

class EditAccountForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.account = self.user.account

        if self.account:
            if self.account.userType.nameUserType == "Natural Person":
                self.fields['first_name'].initial = self.account.personAccount.firstName
                self.fields['last_name'].initial = self.account.personAccount.lastName
            else:
                self.fields['business_name'].initial = self.account.bussinessAccount.nameBussiness

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if any([current_password, new_password1, new_password2]):
            if not all([current_password, new_password1, new_password2]):
                self.add_error('current_password', "You must complete all password fields to change it.")
            
            elif current_password and not self.user.check_password(current_password):
                self.add_error('current_password', "The current password is incorrect.")
            
            elif new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error('new_password2', "The new passwords do not match.")

        return cleaned_data

    def save(self):
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            self.user.set_password(new_password)
        self.user.save()

        if self.account:
            if self.account.userType.nameUserType == "Natural Person":
                np = self.account.personAccount
                np.firstName = self.cleaned_data.get('first_name', '')
                np.lastName = self.cleaned_data.get('last_name', '')
                np.save()

            else:
                bp = self.account.bussinessAccount
                bp.nameBussiness = self.cleaned_data.get('business_name', '')
                bp.save()

        return self.user

    
    current_password = forms.CharField(
        label="Actual password",
        widget=forms.PasswordInput,
        required=False
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,
        required=False
    )

    first_name = forms.CharField(label="Name", required=False)
    last_name = forms.CharField(label="Last name", required=False)

    business_name = forms.CharField(label="Bussiness Name", required=False)

