from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

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
    def generate_slots(cls, start_date, end_date, start_time=datetime.time(9, 0), end_time=datetime.time(18, 0), interval=60, manager=None):
        """
        Генерация слотов на указанный диапазон дат и времени с заданным интервалом.

        :param start_date: Начальная дата диапазона
        :param end_date: Конечная дата диапазона
        :param start_time: Время начала рабочего дня (по умолчанию 9:00)
        :param end_time: Время окончания рабочего дня (по умолчанию 18:00)
        :param interval: Интервал между слотами в минутах (по умолчанию 60 минут)
        :param manager: Менеджер, которому назначаются слоты (по умолчанию None)
        """
        current_date = start_date
        while current_date <= end_date:
            current_time = datetime.datetime.combine(current_date, start_time)
            end_time_combined = datetime.datetime.combine(current_date, end_time)

            while current_time <= end_time_combined:
                # Создаем новый слот, если его еще нет
                cls.objects.get_or_create(
                    date=current_date,
                    time=current_time.time(),
                    defaults={'is_booked': False, 'manager': manager}
                )
                # Увеличиваем текущее время на интервал
                current_time += datetime.timedelta(minutes=interval)

            # Переход к следующей дате
            current_date += datetime.timedelta(days=1)