from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_view),
    path('login', views.login_view),
    path('get_csrf_token', views.get_csrf_token),
    path('testAuthentication', views.testAuthentication_view),
    path('change_password', views.changePassword_view),
]