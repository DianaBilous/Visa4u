from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.management import call_command
from .models import AvailableSlot, Consultation

# Существующее отображение модели Consultation
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'date', 'time', 'status', 'assigned_manager', 'zoom_link')
    list_filter = ('status', 'date', 'assigned_manager')
    search_fields = ('user__username', 'topic')
    ordering = ('-date',)

    # Метод для обработки исключений валидации в админке
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Выполняем валидацию модели
        except ValidationError as e:
            form.add_error(None, e)  # Добавляем ошибку в форму админки
        else:
            super().save_model(request, obj, form, change)

# Добавление функционала для слотов
@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_booked', 'manager')
    list_filter = ('date', 'is_booked')
    search_fields = ('date', 'time')


    # Добавляем URL для кастомного действия
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-slots/', self.admin_site.admin_view(self.generate_slots_view), name='generate_slots'),
        ]
        return custom_urls + urls

    # Представление для вызова команды
    def generate_slots_view(self, request):
        try:
            # Вызываем команду generate_slots
            call_command('generate_slots')
            messages.success(request, 'Свободные слоты успешно сгенерированы!')
        except Exception as e:
            messages.error(request, f'Ошибка при генерации слотов: {e}')

        # Возвращаемся на страницу списка объектов после выполнения команды
        return redirect('admin:consultations_availableslot_changelist')

    # Добавляем кнопку на страницу списка объектов
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_slots_url'] = 'admin:generate_slots'
        return super().changelist_view(request, extra_context=extra_context)