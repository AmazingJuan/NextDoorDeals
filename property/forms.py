from django import forms
from .utilities import getSES, getTypes, getDistricts
from django_flatpickr.widgets import DatePickerInput
from django_flatpickr.schemas import FlatpickrOptions
import datetime
from .models import District, PropertyType
from django.contrib.gis import forms
from mapwidgets.widgets import GoogleMapPointFieldWidget


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
                            label = "District: "
                            )
    pictures = MultipleFileField()
    location = forms.PointField(widget=GoogleMapPointFieldWidget)

    
#Para seleccionar las fechas
class DateForm(forms.Form):
    def __init__(self, *args, disabled_dates=None, **kwargs):
        super().__init__(*args, **kwargs)
        options = FlatpickrOptions(
            minDate=datetime.date.today().strftime('%Y-%m-%d'),
            disable=[
                d.strftime('%Y-%m-%d') if isinstance(d, datetime.date) else d 
                for d in (disabled_dates or [])
            ]
        )
        self.fields['date'].widget = DatePickerInput(options=options)

    date = forms.DateField()



class EditPropertyForm(forms.Form):
    title = forms.CharField(
        label="Property Title:",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control', 'placeholder': 'Enter description'}),
        label="Description:"
    )

    propertyType = forms.ChoiceField(
        choices=[(pt.id, pt.name) for pt in PropertyType.objects.all()],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Property Type:"
    )

    SES = forms.ChoiceField(
        choices=[(ses, ses) for ses in ['1', '2', '3', '4', '5', '6']],  # Modificar según los valores que tengas
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="SES:"
    )

    location = forms.ChoiceField(
        choices=[(district.id, district.name) for district in District.objects.all()],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="District:"
    )

    image = MultipleFileField(
        label="Update Property Images",
        required=False  # No es obligatorio subir nuevas imágenes
    )
    price = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        label="Price:"
    )