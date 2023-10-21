import random
from string import ascii_uppercase, digits

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from users.models import User


def generatestr():
    str0= random.sample(ascii_uppercase,1)+random.sample(digits,3)+random.sample(ascii_uppercase,2)
    return ''.join(str0)


class Order(models.Model):
    ORDER_STATUS = (
        ('Waiting', 'Waiting',),
        ('Processed', 'Processed',),
    )

    code = models.CharField(db_index=True, max_length=6, unique=True, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generatestr()
        super(Order, self).save(*args, **kwargs)


class AttachmentOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(null=True, blank=True, upload_to="files/order/")