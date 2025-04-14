from django.urls import path
from . import views

urlpatterns = [
    path('students/search', views.searchStudent),
    path('mentors/search', views.searchMentor),
    path('students', views.getStudents),
    path('mentors', views.getMentors),
]