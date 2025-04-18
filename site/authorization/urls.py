from django.urls import path
from . import views
from .views import RegisterAPIView, Login_APIView, changePassword_APIView, testAuthentication_APIView, Get_CSRF_token_APIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', Login_APIView.as_view()),
    path('get_csrf_token', Get_CSRF_token_APIView.as_view()),
    path('testAuthentication', testAuthentication_APIView.as_view()),
    path('change_password', changePassword_APIView.as_view()),
]