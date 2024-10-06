from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('in_progress', 'В обработке'),
        ('resolved', 'Решен'),
        ('closed', 'Закрыт'),
    ]

    TYPE_CHOICES = [
        ('support', 'Поддержка'),
        ('technical', 'Технический вопрос'),
        ('order_issue', 'Проблема с заказом'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255, verbose_name="Тема тикета")
    description = models.TextField(verbose_name="Описание проблемы")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Статус тикета")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип тикета")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} к тикету {self.ticket.id}"
