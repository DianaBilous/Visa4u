from django.contrib import admin
from .models import Ticket, TicketComment

# Register your models here.

# Регистрация комментариев для тикетов
admin.site.register(TicketComment)

# Регистрация тикетов с настройками админки
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'description')
    actions = ['mark_as_closed']

    # Экшн для изменения статуса на "Закрыт"
    @admin.action(description="Закрыть выбранные тикеты")
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')

admin.site.register(Ticket, TicketAdmin)

