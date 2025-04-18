from django.http import JsonResponse
from authorization.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization.serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import FoundUserSerializer



class searchStudent_APIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='username',
                type=OpenApiTypes.STR,
                description='',
                required=True,  # Параметр не обязателен
            ),
        ]
    )
    def get(self, request):
        username = request.GET.get("username")
        user = User.objects.filter(username=username).filter(position="student")
        print(user)
        if user.exists():
            return Response(FoundUserSerializer(user, many=True).data, status=200)
        else:
            return Response({"error": "Нет такого студента"}, status=400)
            

class SearchMentor_APIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='username',
                type=OpenApiTypes.STR,
                description='',
                required=True,  # Параметр не обязателен
            ),
        ]
    )
    def get(self, request):
        username = request.GET.get("username")
        user = User.objects.filter(username=username).filter(position="mentor")
        if user.exists():
            return Response(FoundUserSerializer(user, many=True).data, status=200)
        else:
            return Response({"error": "Нет такого ментора"}, status=400)


class getStudents_APIview(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                description='Номер страницы для отображения списка студентов.',
                required=False,  # Параметр не обязателен
            ),
        ]
    )
    def get(self, request):
        User = get_user_model()
        querySet = User.objects.filter(position='student')
        page = request.query_params.get("page")
        paginator = Paginator(querySet, 5)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        return Response({"students": UserSerializer(students, many=True).data})
        


class GetMentors_APIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                description='Номер страницы для отображения списка менторов.',
                required=False,  # Параметр не обязателен
            ),
        ]
    )
    def get(self, request):
        querySet = User.objects.filter(position="mentor")
        page = request.GET.get("page")
        paginator = Paginator(querySet, 5)
        try:
            mentors = paginator.page(page)
        except PageNotAnInteger:
            mentors = paginator.page(1)  # Если page не число, возвращаем первую страницу
        except EmptyPage:
            mentors = paginator.page(paginator.num_pages)  # Если page за пределами диапазона, возвращаем последнюю страницу
        
        return Response({"mentors": UserSerializer(mentors, many=True).data}, status=200)
    
