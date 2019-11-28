from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser


class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(unique=True, primary_key=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=40)

    first_name = models.CharField(default='', max_length=15)
    last_name = models.CharField(default='', max_length=15)
    login = models.CharField(max_length=15)
    age = models.IntegerField()
    street = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    zip = models.CharField(blank=True, max_length=10)
    role = models.CharField(default='', max_length=10)
    locked = models.BooleanField(blank=True)

    USERNAME_FIELD = 'id'


class UserSettings(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              primary_key=True)
    theme = models.CharField(max_length=10)
