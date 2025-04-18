from authorization.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
# Create your views here.



@method_decorator(csrf_protect, name='dispatch')
class AttachMentor_APIView(APIView):
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'student_username': {'type': 'string', 'description': 'Первое поле'},
                    'mentor_username': {'type': 'string', 'description': 'Второе поле'},
                },
                'required': ['student_username', 'mentor_username']
            }
        },
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        try:
            student_username = request.data.get("student_username")
            mentor_username = request.data.get("mentor_username")
            student = User.objects.get(username=student_username)
            mentor = User.objects.get(username=mentor_username)
            student.mentor = mentor
            student.save()
            return Response({"message": f"студент {student_username} был прикреплён к ментору {mentor_username}"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Студент или ментор не найдены"},  status=404)

        