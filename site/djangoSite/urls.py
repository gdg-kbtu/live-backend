from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('main/', include('main.urls')),
    path('cabinet/', include('personalCabinet.urls')),
    path('auth/', include('authorization.urls')),
    path('admin/', admin.site.urls),
]
