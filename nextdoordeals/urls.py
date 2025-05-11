"""
URL configuration for nextdoordeals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from property.views import error
from account.views import logout_logic, loginUser, show_appointments
from django.conf.urls.static import static
from django.conf import settings
from account import consumers
from account.views import send_message
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('property.urls')),
    path('error/', error, name='error'),
    path('logout/', logout_logic, name = 'logout'),
    path('login/', loginUser, name = 'login'),
    path('appointments/', show_appointments, name = 'appointments'),
    path('send_message/', send_message, name='send_message'),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]