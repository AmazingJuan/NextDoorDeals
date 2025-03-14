from django import forms
from .utilities import getSES

class PublishForm(forms.Form):

    title = forms.CharField(label = "Property Title: ")
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':5, 'cols':40, 'class':'form-control'}), label = "Description: "  )
    SES = forms.ChoiceField(choices=getSES, widget = forms.Select(), label = "SES: ", label_suffix="")
    price = forms.IntegerField(label = "Price: ")
    pictures = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    