from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models


class Role(Enum):
    DONOR = 'donor'
    RECEIVER = 'receiver'


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[(role.value, role.name) for role in Role])

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'role']

    def __str__(self):
        return f"{self.name} - {self.role} - {self.email} - {self.Phone_number} - {self.username}"