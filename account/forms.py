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

class EditAccountForm(forms.ModelForm):

    current_password = forms.CharField(
        label="Actual Password",
        widget=forms.PasswordInput,
        required=False
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['username']
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # Validación para cambio de contraseña
        if any([current_password, new_password1, new_password2]):
            if not all([current_password, new_password1, new_password2]):
                raise ValidationError("Debes completar todos los campos de contraseña para cambiarla.")
            
            if not self.user.check_password(current_password):
                self.add_error('current_password', "La contraseña actual es incorrecta.")
            
            if new_password1 != new_password2:
                self.add_error('new_password2', "Las nuevas contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Actualizar contraseña si se proporcionó
        if self.cleaned_data['new_password1']:
            user.set_password(self.cleaned_data['new_password1'])
        
        if commit:
            user.save()
        
        return user
 
