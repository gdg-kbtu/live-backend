from django.urls import path 
from . import views
from .views import AttachMentor_APIView

urlpatterns = [
    path('attachMentor', AttachMentor_APIView.as_view())
]
