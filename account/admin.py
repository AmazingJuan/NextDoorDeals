from django.contrib import admin
from .models import Account, UserType, Role, PersonAccount, BussinessAccount, Subscription

# Register your models here.

admin.site.register(Account)
admin.site.register(UserType)
admin.site.register(Role)
admin.site.register(PersonAccount)
admin.site.register(BussinessAccount)
admin.site.register(Subscription)