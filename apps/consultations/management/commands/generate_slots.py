from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.consultations.models import AvailableSlot
import datetime

class Command(BaseCommand):
    help = 'Генерирует свободные слоты для консультаций на следующие 7 дней'

    def handle(self, *args, **kwargs):
        # Определяем начальную и конечную даты для генерации
        today = timezone.now().date()
        end_date = today + timezone.timedelta(days=7)   # создаем слоты на 7 дней вперед
        start_time = datetime.time(9, 0)
        end_time = datetime.time(18, 0)
        interval = 60  # Интервал в минутах
        
        current_date = today
        while current_date <= end_date:
            current_time = datetime.datetime.combine(current_date, start_time)
            end_time_combined = datetime.datetime.combine(current_date, end_time)

            while current_time <= end_time_combined:
                AvailableSlot.objects.get_or_create(
                    date=current_date,
                    time=current_time.time(),
                    defaults={'is_booked': False}
                )
                current_time += datetime.timedelta(minutes=interval)

            current_date += datetime.timedelta(days=1)
        
        # Сообщение успешного выполнения
        self.stdout.write(self.style.SUCCESS('Свободные слоты успешно сгенерированы'))
