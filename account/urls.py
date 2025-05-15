from django.urls import path
from . import views
import account.consumers as consumers

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/success/', views.signupSuccess, name='SUsuccess'),
    path('cancel_subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('get_chat_history/<str:username>/', views.get_chat_history, name='get_chat_history'),
    path('<str:username>/editProfile/', views.edit_profile, name='editProfile'),
    path('<str:username>/', views.view_profile, name='view_profile'),
]

websocket_urlpatterns = [
    path("ws/chat/<str:username>/", consumers.ChatConsumer.as_asgi()),  # Conexión WebSocket
]