from authorization.models import User
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

# Create your views here.


@require_POST
def attachMentor(request):
    model = get_user_model()

    params = request.POST
    studentID_student = params.get("studentID_student")
    studentID_mentor = params.get("studentID_mentor")
    try:
        student = get_object_or_404(model, studentID=studentID_student)
        mentor = get_object_or_404(model, studentID=studentID_mentor, position="mentor")
        student.mentor = mentor
        student.save()
        return JsonResponse({"message": f"студент {student.username} был прикреплён к ментору {mentor.username}"})
    except User.DoesNotExist:
        return JsonResponse({"error": "Студент или ментор не найдены"},  status=404)
    except Exception as e:
        return JsonResponse({"error": f"произошла ошибка: {e}"}, status=500)
        