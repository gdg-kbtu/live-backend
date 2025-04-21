from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    studentID = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=10, choices=[('mentor', 'Mentor'), ('student', 'Student')])
    mentor = models.ForeignKey('self', to_field='studentID', related_name='students', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'position': 'mentor'})
    projects = models.ManyToManyField('authorization.Project', blank=True, related_name='contributors')


class Project(models.Model):
    projectID = models.CharField(unique=True)
    name = models.CharField()
    description = models.CharField(null=True, blank=True)
    github_url = models.CharField()

class Commit(models.Model):
    commitID = models.CharField(unique=True)
    details = models.CharField(null=True, blank=True)
    commitAuthor = models.CharField()
    project = models.ForeignKey('authorization.Project', to_field='projectID', on_delete=models.SET_NULL, null=True, blank=True, related_name='commits')
    