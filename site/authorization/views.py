from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

# Create your views here.

def get_csrf_token(request):
   csrf_token = get_token(request)
   return JsonResponse({
      "csrf_token": csrf_token
   })

@csrf_exempt
def register_view(request):
   if request.method == "POST":
      params = request.POST
      username = params.get("username")
      password = params.get("password")
      password2 = params.get("password2")
      if(password != password2):
         return JsonResponse({"error": "пароли не совпадают"}, status=400)
      
      try:
         user = User.objects.create_user(username=username, password=password)
         login(request, user)
         return JsonResponse({"message": f"пользователь {username} успешно зарегистрирован"}, status=200)
      except Exception as e:
         if "повторяющееся значение ключа нарушает ограничение уникальности" in str(e):
            return JsonResponse({"error": "Это имя уже занято"}, status=400)
         else:
            return JsonResponse({"error:": f"Произошла ошибка {e}"}, status=500)
   else:
      return JsonResponse({"error: ", "неверный метод запроса"}, status=400)
  
@csrf_exempt
def login_view(request):
   try:
       if request.method == "POST":
           params = request.POST
           username = params.get("username")
           password = params.get("password")

           user = authenticate(request, username=username, password=password)

           if user is not None:
              login(request, user)
              return JsonResponse({"message": "Вход выполнен успешно"}, status=200)
           else:
              return JsonResponse({"error": "Неверные учетные данные"}, status=401)
       else:
           return JsonResponse({"error": "Неверный метод запроса"}, status=405)
   except Exception as e:
       return JsonResponse({"error", f"Произошла ошибка: {e}"}, status=500)





def testAuthentication_view(request):
   if request.user.is_authenticated:
      return JsonResponse({"message": "Доступ разрешён"}, status=200)
   else:
      return JsonResponse({"error": "Необходима аутентификация"}, status=401)

@csrf_exempt
def changePassword_view(request):
   if request.method == "POST":
      try:
         if request.user.is_authenticated:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            if check_password(current_password, request.user.password):
               request.user.set_password(new_password)
               request.user.save()

               #переаутентификация
               user = authenticate(request, username=request.user.username, password=new_password)
               if user is not None:
                  login(request, user)
               return JsonResponse({"message": "Пароль успешно изменён"}, status=200)
            else:
               return JsonResponse({"error": "Неверный текущий пароль"}, status=400)
         else:
            return JsonResponse({"error": "Необходима аутентификация"}, status=401)
      except Exception as e:
         return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)
   else:
      return JsonResponse({"error": "Неверный метод запроса"}, status=400)


   
