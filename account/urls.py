from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.signup, name = 'signup'),
    path('signup/success/', views.signupSuccess, name = 'SUsuccess'),
    path('<str:username>/', views.view_profile, name = 'view_profile'),
    path('<str:username>/editProfile/', views.edit_profile, name='edit_profile'),
    ]