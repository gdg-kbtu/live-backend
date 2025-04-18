
from django.urls import path 
from . import views
from .views import GetPersonalData_APIView

urlpatterns = [
    path('getPersonalData', GetPersonalData_APIView.as_view())
]
