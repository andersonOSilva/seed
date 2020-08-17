from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.core import validators

from django.utils import timezone

import re
import crypt


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model de usuários.
    """
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=400)
    email = models.CharField(max_length=200, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    def check_password(self, password):
        if self.password == crypt.crypt(password,"$6$salt$"):
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        # criptografa password
        self.password = crypt.crypt(self.password,"$6$salt$")
        super(User, self).save(*args, **kwargs)
