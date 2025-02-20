from django.contrib import admin
from .models import Property
from .models import City
from .models import Province
from .models import Neighborhood
from .models import Address
from .models import District
# Register your models here.

admin.site.register(Property)
admin.site.register(City)
admin.site.register(Province)
admin.site.register(Neighborhood)
admin.site.register(Address)
admin.site.register(District)

