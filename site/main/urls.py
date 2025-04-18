from django.urls import path
from . import views
from .views import getStudents_APIview, searchStudent_APIView, SearchMentor_APIView, GetMentors_APIView

urlpatterns = [
    path('students/search', searchStudent_APIView.as_view()),
    path('mentors/search', SearchMentor_APIView.as_view()),
    path('students', getStudents_APIview.as_view()),
    path('mentors', GetMentors_APIView.as_view()),
]