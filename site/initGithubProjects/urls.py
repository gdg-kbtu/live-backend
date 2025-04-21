from django.urls import path
from . import views
from .views import initRepo_APIView

urlpatterns = [
    path('initRepo', initRepo_APIView.as_view())
]