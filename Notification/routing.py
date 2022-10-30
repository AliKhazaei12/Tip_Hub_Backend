from django.urls import path
from .consumers import Notificationconsumer

websocket_urlpatterns =[
    path('ws/notification/',Notificationconsumer.as_asgi()),

]