from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Custom User model to test user conditions
class MyUserModel(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True)
    USERNAME_FIELD = "identifier"
