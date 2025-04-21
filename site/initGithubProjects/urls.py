from django.urls import path
from . import views
from .views import initRepo_APIView, getRepos_APIView, getRepoCommits_APIView

urlpatterns = [
    path('initRepo', initRepo_APIView.as_view()),
    path('getRepos', getRepos_APIView.as_view()),
    path('getCommits', getRepoCommits_APIView.as_view())
]