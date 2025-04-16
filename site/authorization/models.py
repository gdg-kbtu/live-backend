from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    studentID = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=10, choices=[('mentor', 'Mentor'), ('student', 'Student')])
    mentor = models.ForeignKey('self', related_name='students', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'position': 'mentor'})
