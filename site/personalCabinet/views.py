from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
# Create your views here.

@csrf_exempt
@require_GET
def getPersonalData(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "необходима аутентификация"}, status=401)
    
    try:
        user = User.objects.get(username=request.user.username)
        userData = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            # Добавьте другие поля по мере необходимости
        }
        return JsonResponse(userData, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "пользователь не найден"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"произошла ошибка: {e}"}, status=500)