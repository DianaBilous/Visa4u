from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Consultation(models.Model):
    """Модель для хранения заказов на консультации"""

    STATUS_CHOICES = [
        ('paid', 'Оплачена'),
        ('manager_assigned', 'Менеджер назначен'),
        ('time_to_confirm', 'Согласование времени'),
        ('time_scheduled', 'Время назначено'),
        ('service_provided', 'Услуга оказана'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    full_name = models.CharField(max_length=255, default='', verbose_name="ФИО")
    topic = models.CharField(max_length=255, verbose_name="Тема консультации")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=7000)  # Цена консультации
    date = models.DateField(verbose_name="Дата консультации")
    time = models.TimeField(verbose_name="Время консультации")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid', verbose_name="Статус консультации")
    assigned_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_consultations')
    zoom_link = models.URLField(max_length=255, blank=True, null=True, verbose_name="Ссылка на Zoom комнату")  # Поле для Zoom ссылки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Консультация {self.topic} с {self.user.username} на {self.date} в {self.time}"
    

class AvailableSlot(models.Model):
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    is_booked = models.BooleanField(default=False, verbose_name="Занято")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Менеджер")

    def __str__(self):
        return f"{self.date} {self.time} {'(Занято)' if self.is_booked else '(Свободно)'}"

    @classmethod
    def generate_slots(cls, start_date, end_date):
        """Генерация слотов с 9:00 до 19:00 (с шагом в 1 час) на указанный диапазон дат"""
        for single_date in (start_date + timezone.timedelta(days=n) for n in range((end_date - start_date).days + 1)):
            for hour in range(9, 19):
                time = timezone.datetime.combine(single_date, timezone.time(hour, 0)).time()
                cls.objects.get_or_create(date=single_date, time=time)