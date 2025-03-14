from django.urls import path
from .views import home, publish
urlpatterns = [path('', home, name = 'home'), path('publish/', publish) ]