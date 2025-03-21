from django import forms
from .utilities import getSES, getTypes, getDistricts

#CODIGO EXTRAIDO DE LA DOCUMENTACIÓN DE DJANGO: https://docs.djangoproject.com/en/5.0/topics/http/file-uploads/#uploading-multiple-files

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


# CODIGO PROPIO A PARTIR DE AKA
class PublishForm(forms.Form):
    title = forms.CharField(label = "Property Title: ")
    description = forms.CharField(
        widget = forms.Textarea(attrs={'rows':5, 'cols':40, 'class':'form-control'}), 
        label = "Description: "  )
    SES = forms.ChoiceField(choices=getSES, widget = forms.Select(), 
                            label = "SES: "
                            )
    type = forms.ChoiceField(choices=getTypes, widget = forms.Select(), 
                            label = "Type: "
                            )
    price = forms.IntegerField(label = "Price: ")
    district = forms.ChoiceField(choices=getDistricts, widget = forms.Select(), 
                            label = "Type: "
                            )
    pictures = MultipleFileField()
    

    