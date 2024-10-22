from django.contrib import admin
from .models import Consultation, AvailableSlot

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'date', 'time', 'status', 'assigned_manager', 'zoom_link')
    list_filter = ('status', 'date', 'assigned_manager')
    search_fields = ('user__username', 'topic')
    ordering = ('-date',)
    
@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'is_booked')
    list_filter = ('date', 'is_booked')
    search_fields = ('date', 'time')