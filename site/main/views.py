from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@csrf_exempt
@require_GET
def searchStudent(request):
    username = request.GET.get("username")
    try:
        group = Group.objects.get(name="mentor")
        user = User.objects.exclude(groups=group).filter(username=username)
        if user.exists():
            student_data = {
                "id": user[0].id,
                "username": user[0].username,
            }
            return JsonResponse({"data": student_data}, status=200)
        else:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)
    
@csrf_exempt
@require_GET
def searchMentor(request):
    username = request.GET.get("username")
    try:
        group = Group.objects.get(name="mentor")
        user = User.objects.filter(groups=group).filter(username=username)
        if user.exists():
            mentor_data = {
                "id": user[0].id,
                "username": user[0].username,
            }
            return JsonResponse({"data": mentor_data}, status=200)
        else:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)

@csrf_exempt
@require_GET
def getStudents(request):
    try:
        group = Group.objects.get(name="mentor")
        users = User.objects.exclude(groups=group)

        page = request.GET.get("page")
        paginator = Paginator(users, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)  # Если page не число, возвращаем первую страницу
        except EmptyPage:
            users = paginator.page(paginator.num_pages)  # Если page за пределами диапазона, возвращаем последнюю страницу
        
        students_data  = []
        for user in users:
            students_data.append({
                "id": user.id,
                "username": user.username
            })
        
        return JsonResponse({"data": students_data,
                             "page": users.number,
                             "num_pages": paginator.num_pages}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)
    
@csrf_exempt
@require_GET
def getMentors(request):
    try:
        group = Group.objects.get(name="mentor")
        users = User.objects.filter(groups=group)

        page = request.GET.get("page")
        paginator = Paginator(users, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)  # Если page не число, возвращаем первую страницу
        except EmptyPage:
            users = paginator.page(paginator.num_pages)  # Если page за пределами диапазона, возвращаем последнюю страницу
        
        mentors_data  = []
        for user in users:
            mentors_data.append({
                "id": user.id,
                "username": user.username
            })
        
        return JsonResponse({"data": mentors_data,
                             "page": users.number,
                             "num_pages": paginator.num_pages}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Произошла ошибка: {e}"}, status=500)
