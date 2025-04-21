from authorization.models import User, Project, Commit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization.serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import requests
from django.contrib.auth import authenticate

class getRepoCommits_APIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='repo_name',
                type=OpenApiTypes.STR,
                description='Имя репозитория для получения его коммитов',
                required=True,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def get(self, request):
        repo_name = request.query_params.get("repo_name")
        repo = Project.objects.get(name=repo_name)
        commits_data = []
        commits = repo.commits.all()
        for commit in commits:
            commits_data.append({
                "id": commit.commitID,
                "details": commit.details,
                "commitAuthor": commit.commitAuthor
            })
        return Response(commits_data, status=200)
    

# Create your views here.
class getRepos_APIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='username',
                type=OpenApiTypes.STR,
                description='Имя пользователя для получения его репозиториев',
                required=True,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def get(self, request):
        try:
            username = request.query_params.get("username")
            user = User.objects.get(username=username)
            projects = user.projects.all()
            projects_serialized = []
            for project in projects:
                projects_serialized.append({
                    "project_id": project.projectID,
                    "name": project.name,
                    "description": project.description,
                    "github_url": project.github_url
                })
            return Response(projects_serialized, status=200)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=400)


class initRepo_APIView(APIView):
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'github_username': {'type': 'string', 'description': 'Имя пользователя GitHub'},
                    'repos_name': {'type': 'string', 'description': 'Название репозитория GitHub'},
                    'headers': {
                        'type': 'object',
                        'description': 'Произвольные HTTP-заголовки для запроса к GitHub API',
                        'example': {
                            'X-CSRFToken': 'value'
                        }
                    },
                },
                'required': ['github_username', 'repos_name'],
            }
        }
    )
    def post(self, request):
        if request.user.is_authenticated is not True:
            return Response({"error": "Необходима аутентификация"}, status=400)
        
        params = request.data
        github_username = params.get("github_username")
        repos_name = params.get("repos_name")
        try:
            # достаём репозиторий
            response = requests.get(f"https://api.github.com/repos/{github_username}/{repos_name}")
            response.raise_for_status()
            data = response.json()  # десериализуем тело ответа.
            created_project = Project.objects.create(**{
                "projectID": data.get("id"),
                "name": repos_name,
                "description": data.get("description"),
                "github_url": data.get("html_url")
            })
            
            # достаём коммиты
            response2 = requests.get(f"https://api.github.com/repos/{github_username}/{repos_name}/commits")
            response2.raise_for_status()
            commits = response2.json()
            commits_to_create = []
            for commit in commits:
                commits_to_create.append(Commit(
                    commitID=commit.get("sha"),
                    details=commit.get("commit").get("message"),
                    commitAuthor=commit.get("commit").get("author"),
                    project=created_project
                ))
            # создаём сразу лист коммитов, а не кучу отдельных коммитов.  Так лучше для Django ORM.
            Commit.objects.bulk_create(commits_to_create)
            
            user = request.user
            # используем add() для привязывания проекта к юзерам по связи многие-ко-многим.
            user.projects.add(created_project)
            
            return Response({"message": f"Репозиторий успешно добавлен и привязан к пользователю {request.user.username}"}, status=200)

        except requests.exceptions.RequestException as e:
            return Response({"error": e}, status=500)