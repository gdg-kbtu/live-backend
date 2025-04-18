from rest_framework import serializers
from .models import User



class UserRegistrationSerializer(serializers.Serializer):
    studentID = serializers.CharField(max_length=10)
    position = serializers.CharField(max_length=10)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Новые пароли не совпадают.")
        return data

class UserSerializer(serializers.Serializer):
    studentID = serializers.CharField(max_length=10)
    position = serializers.CharField(max_length=10)
    mentor_id = serializers.IntegerField(allow_null=True, required=False)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})


    def update(self, instance, validated_data):
        instance.studentID = validated_data.get('studentID', instance.studentID)
        instance.position = validated_data.get('position', instance.position)
        instance.mentor_id = validated_data.get('mentor_id', instance.mentor_id)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance