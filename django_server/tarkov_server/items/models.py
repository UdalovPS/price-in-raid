from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip = models.TextField(max_length=50, null=True, blank=True)
    pay_date = models.DateField(null=True, blank=True)
    use_date = models.DateField(null=True, blank=True)
    verification = models.BooleanField(default=False)
    language = models.CharField(max_length=3, default='eng')
    token = models.CharField(max_length=10, null=True, blank=True)


class Tmp(models.Model):
    test = models.CharField(max_length=10, default="test")
    number = models.IntegerField(default=10)
