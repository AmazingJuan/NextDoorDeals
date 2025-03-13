from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.signup, name = 'signup'),
    path('signup/success/', views.signupSuccess, name = 'SUsuccess')


]