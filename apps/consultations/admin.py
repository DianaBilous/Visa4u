from django.contrib import admin
from .models import AvailableSlot, Consultation
from django.contrib import messages
import datetime

# Существующее отображение модели Consultation
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'date', 'time', 'status', 'assigned_manager', 'zoom_link')
    list_filter = ('status', 'date', 'assigned_manager')
    search_fields = ('user__username', 'topic')
    ordering = ('-date',)

# Добавление функционала для слотов
@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_booked', 'manager')
    list_filter = ('date', 'is_booked')
    search_fields = ('date', 'time')

    # Добавляем действие для генерации слотов
    actions = ['generate_slots']

    # Определение кастомного действия
    def generate_slots(self, request, queryset):
        if 'apply' in request.POST:
            # Получаем данные из формы
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            interval = int(request.POST.get('interval', 60))  # Интервал в минутах

            # Конвертируем строки в объекты datetime
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
                end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

                current_date = start_date
                while current_date <= end_date:
                    current_time = datetime.datetime.combine(current_date, start_time)
                    end_time_combined = datetime.datetime.combine(current_date, end_time)

                    while current_time <= end_time_combined:
                        # Создаем новый слот
                        AvailableSlot.objects.create(
                            date=current_date,
                            time=current_time.time(),
                            is_booked=False,
                            manager=request.user  # Назначаем текущего менеджера
                        )
                        # Увеличиваем текущее время на интервал
                        current_time += datetime.timedelta(minutes=interval)

                    current_date += datetime.timedelta(days=1)

                messages.success(request, 'Слоты успешно сгенерированы!')
                return redirect(request.get_full_path())  # Возвращаемся на ту же страницу после генерации слотов

            except Exception as e:
                messages.error(request, f'Ошибка: {e}')
                return redirect(request.get_full_path())  # Возвращаемся на ту же страницу после ошибки

        # Если это GET-запрос, показываем форму с полями
        self.message_user(request, "Для генерации слотов заполните форму ниже.")
        form_html = '''
            <form method="post" style="padding: 10px;">
                <label>Начальная дата:</label><br>
                <input type="date" name="start_date" required><br><br>
                <label>Конечная дата:</label><br>
                <input type="date" name="end_date" required><br><br>
                <label>Начальное время:</label><br>
                <input type="time" name="start_time" required><br><br>
                <label>Конечное время:</label><br>
                <input type="time" name="end_time" required><br><br>
                <label>Интервал (минуты):</label><br>
                <input type="number" name="interval" value="60" required><br><br>
                <button type="submit" name="apply" class="btn btn-primary">Сгенерировать слоты</button>
            </form>
        '''
        self.message_user(request, form_html, level=messages.INFO)