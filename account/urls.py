from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.signup, name = 'signup'),
    path('signup/success/', views.signupSuccess, name = 'SUsuccess'),
    path('login/', views.loginUser, name = 'login'),
    path('<str:username>/', views.view_profile, name = 'view_profile'),
    path('logout/', views.logout_logic, name = 'logout'),
    ]