from django.urls import path
from .views import send_notification
app_name='Notification'
urlpatterns = [
    path('user/<int:user_id>/send_notification/',send_notification, name='send_notification')
]