from django.urls import path
from .views import home, publish, view_property, schedule_appointment, favourite
urlpatterns = [path('', home, name = 'home'), 
               path('publish/', publish, name = 'publish'),
                path('<int:id>/', view_property, name = 'property_info'),
                path('<int:id>/appointment/', schedule_appointment, name = "appointment"),
                path('<int:id>', favourite, name = 'makeFavourite' ),]