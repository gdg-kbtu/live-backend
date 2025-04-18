from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from authorization.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# Create your views here.


class RegisterAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                login(request, user)
                return Response({"message": f"пользователь {user.username} успешно зарегистрирован"}, status=200)
            except Exception as e:
                print(e)
                if "повторяющееся значение ключа нарушает ограничение уникальности \"authorization_user_username_key\"" in str(e):
                    return Response({"error": "Этот username уже занят"}, status=400)
                elif "повторяющееся значение ключа нарушает ограничение уникальности \"authorization_user_studentID_key\"" in str(e):
                    return Response({"error": "Этот studentID уже занят"}, status=400)
                else:
                    return Response({"error:": f"Произошла ошибка {e}"}, status=500)
        return Response(serializer.errors, status=400)
        


class Get_CSRF_token_APIView(APIView):
   def get(self, request):
      csrf_token = get_token(request)
      return Response({"csrf_token": csrf_token})



class Login_APIView(APIView):
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'Первое поле'},
                    'password': {'type': 'string', 'description': 'Второе поле'},
                },
                'required': ['username', 'password']
            }
        },
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
         username = request.data.get("username")
         print(username)
         password = request.data.get("password")
         user = authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return Response({"message": "Пользователь успешно вошёл в систему"}, status=200)
         else:
            if User.objects.filter(username=username).exists():
               return Response({"error": "Неверный пароль"}, status=400)
            else:
               return Response({"error": "Пользователь с таким именем не найден"}, status=400) 
               




@method_decorator(csrf_protect, name='dispatch')
class testAuthentication_APIView(APIView):
   # @extend_schema(
   #      parameters=[
   #          OpenApiParameter(
   #              name='X-CSRFToken',
   #              type=OpenApiTypes.STR,
   #              description='CSRF токен из куки csrftoken=',
   #              location=OpenApiParameter.HEADER,
   #              required=True,  # Заголовок может быть необязательным
   #          ),
   #      ]
   #  )
   def post(self, request):
      if request.user.is_authenticated:
         return Response({"message": "Доступ разрешён"}, status=200)
      else:
         return Response({"error": "Необходима аутентификация"}, status=401)




@method_decorator(csrf_protect, name='dispatch')
class changePassword_APIView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                current_password = serializer.validated_data.get("current_password")
                new_password = serializer.validated_data.get("new_password")

                if check_password(current_password, request.user.password):
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # Обновляем сессию, чтобы избежать выхода

                    return Response({"message": "Пароль успешно изменён"}, status=200)
                else:
                    return Response({"error": "Неверный текущий пароль"}, status=400)
            else:
                return Response({"error": "Необходима аутентификация"}, status=401)
        else:
            return Response(serializer.errors, status=400)
         
         



   
