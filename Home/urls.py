from django.urls import path
from .views import Homepage

app_name = 'Home'
urlpatterns = [
    path('', Homepage.as_view(), name='home'),


]
