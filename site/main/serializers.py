from rest_framework import serializers
from authorization.models import User






class FoundUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    studentID = serializers.CharField(max_length=20)
    email = serializers.CharField(max_length=40)
    mentor_id = serializers.IntegerField()