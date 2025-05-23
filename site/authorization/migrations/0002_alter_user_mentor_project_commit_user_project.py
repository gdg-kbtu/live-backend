# Generated by Django 5.2 on 2025-04-20 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mentor',
            field=models.ForeignKey(blank=True, limit_choices_to={'position': 'mentor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to=settings.AUTH_USER_MODEL, to_field='studentID'),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectID', models.CharField(unique=True)),
                ('name', models.CharField()),
                ('description', models.CharField(blank=True, null=True)),
                ('github_url', models.CharField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to=settings.AUTH_USER_MODEL, to_field='studentID')),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commitID', models.CharField(unique=True)),
                ('details', models.CharField(blank=True, null=True)),
                ('commitAuthor', models.CharField()),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commits', to='authorization.project', to_field='projectID')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contributors', to='authorization.project', to_field='projectID'),
        ),
    ]
