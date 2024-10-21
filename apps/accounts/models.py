# apps/accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Кто отправил сообщение
    text = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения

    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}"

