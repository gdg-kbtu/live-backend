
from django.urls import path 
from . import views


urlpatterns = [
    path('getPersonalData', views.getPersonalData)
]
