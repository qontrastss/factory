from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    chat_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="ID чата с ботом")
    is_active = models.BooleanField(default=True)


class Message(models.Model):
    telegram = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250, null=True, blank=True)


class TelegramUserConnectTry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    chat_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="ID чата с ботом")
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(null=True, blank=True)