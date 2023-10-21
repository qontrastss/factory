from datetime import datetime, timedelta

import jwt
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from factory import settings
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'phone'
    objects = UserManager()

    def __str__(self):
        return self.phone

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
