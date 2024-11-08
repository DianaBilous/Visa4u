from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Message

def send_admin_message(request, room_name):
    if request.method == "POST":
        text = request.POST.get("text")
        user = request.user
        Message.objects.create(user=user, text=text, room=room_name, is_admin=True)
        return HttpResponseRedirect(reverse('admin:chat_room_view', args=[room_name]))

@admin.register(Message)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'timestamp', 'is_read', 'open_chat_link')
    list_filter = ('is_read', 'user', 'timestamp')
    search_fields = ('text', 'user__username', 'room')

    def open_chat_link(self, obj):
        # Ссылка для перехода в чат комнаты
        return format_html(
            '<a class="button" href="{}">Открыть чат</a>',
            reverse('admin:chat_room_view', args=[obj.room])
        )
    open_chat_link.short_description = 'Открыть чат'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'chat_room/<str:room_name>/send_message/',
                self.admin_site.admin_view(send_admin_message),  # Передаем функцию напрямую
                name='send_admin_message'
            ),
            path(
                'chat_room/<str:room_name>/',
                self.admin_site.admin_view(self.chat_room_view),
                name='chat_room_view'
            ),
            path(
                'chats/',
                self.admin_site.admin_view(self.chat_list_view),
                name='chat_list_view',
            ),
        ]
        return custom_urls + urls

    def chat_list_view(self, request):
        # Получаем список уникальных комнат чатов
        rooms = Message.objects.values('room').distinct()
        return render(request, 'admin/chat/chat_list.html', {'rooms': rooms})

    def chat_room_view(self, request, room_name):
        # Получаем сообщения из указанной комнаты
        messages = Message.objects.filter(room=room_name).order_by('timestamp')
        messages.update(is_read=True)  # Помечаем как прочитанные
        return render(request, 'admin/chat/chat_room.html', {
            'room_name': room_name,
            'messages': messages,
        })
