from datetime import datetime
from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager


"""
class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')
"""


class UserProfile(AbstractUser):
    phone = models.CharField(max_length=11)
    identity_number = models.CharField(max_length=18)
    identity_type = models.CharField(max_length=12)
    level = models.IntegerField(default=1)
    city = models.CharField(max_length=10, default="")
    edit_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=500, default="")
    pass


class Task(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, default="")
    request_population = models.IntegerField()
    end_time = models.DateTimeField()
    photo = models.CharField(max_length=100, default="")
    edit_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)
    pass


class TaskRequest(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    info = models.CharField(max_length=50, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField()
    pass


class FinishTaskDetail(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    creator = models.ForeignKey(get_user_model(), related_name="creator", on_delete=models.CASCADE)
    executor = models.ManyToManyField(get_user_model(), related_name="doer")
    finish_time = models.DateTimeField()
    creator_expense = models.IntegerField()
    executor_expense = models.IntegerField()
    pass


class IncomeSummary(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=10)
    task_type = models.CharField(max_length=5)
    finish_number = models.IntegerField()
    income = models.IntegerField()
    pass
