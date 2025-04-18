from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
# Create your views here.


class GetPersonalData_APIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "необходима аутентификация"}, status=401)
        else:
            response_data = {
                "studentID": request.user.studentID,
                "username": request.user.username,
                "email": request.user.email,
                "position": request.user.position,
                "mentor_id": request.user.mentor_id,
            }
            return Response({"user": response_data}, status=200)
