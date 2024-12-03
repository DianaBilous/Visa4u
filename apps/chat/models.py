from django.contrib.auth.models import User
from django.db import models

# модель для хранения сообщений 
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Кто отправил сообщение
    text = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения
    is_admin = models.BooleanField(default=False) # Флаг для обозначения сообщения от администратора
    is_read = models.BooleanField(default=False) 
    room = models.CharField(max_length=100)  # Название комнаты чата, если требуется

    class Meta:
        verbose_name = "Сообщение"  
        verbose_name_plural = "Сообщения"

    def __str__(self):
        if self.is_admin:
            sender = "Admin"
        else:
            sender = self.user.username if self.user else "Anonymous"
        return f"{sender}: {self.text[:50]}"