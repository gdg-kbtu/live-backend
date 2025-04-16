from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    studentID = serializers.CharField(max_length=10, unique=True)
    position = serializers.CharField(max_length=10, choices=[('mentor', 'Mentor'), ('student', 'Student')])
    mentor_id = serializers.IntegerField(allow_null=True) # Учитываем возможность отсутствия ментора

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False) # Пароль для создания/обновления

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.studentID = validated_data.get('studentID', instance.studentID)
        instance.position = validated_data.get('position', instance.position)
        instance.mentor_id = validated_data.get('mentor_id', instance.mentor_id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance