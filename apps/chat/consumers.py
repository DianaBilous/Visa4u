import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Определение комнаты чата
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Добавляем канал в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Получаем историю сообщений и отправляем клиенту
        messages = await self.get_chat_history(self.room_name)
        for message in messages:
            await self.send(text_data=json.dumps({
                'username': message['user__username'],
                'message': message['text'],
                'timestamp': message['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            }, ensure_ascii=False))

    @database_sync_to_async
    def get_chat_history(self, room_name):
        from .models import Message
        return list(
        Message.objects.filter(room=f'chat_{room_name}').order_by('timestamp').values('user__username', 'text', 'timestamp')
        )

    async def disconnect(self, close_code):
        # Убираем канал из группы при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Локальный импорт модели
        from .models import Message

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # Получаем имя пользователя, если он аутентифицирован
        username = user.username if user.is_authenticated else "Guest"
        
        # Определяем, является ли отправитель администратором
        is_admin = user.is_staff or user.is_superuser if user.is_authenticated else False

        # Сохраняем сообщение в базу данных 
        await database_sync_to_async(Message.objects.create)(
            user=user if user.is_authenticated else None,
            text=message,
            is_admin=is_admin,
            room=self.room_group_name
        )

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': "Admin" if is_admin else username
            }
        )

        # Отправка уведомления для администраторов
        if not is_admin:
            await self.channel_layer.group_send(
                "admin_notifications",
                {
                    "type": "new_message_notification",
                    "message": message,
                    "username": username,
                    "room": self.room_name
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Отправляем сообщение обратно по WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }, ensure_ascii=False))
        

class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_staff:
            await self.channel_layer.group_add("admin_notifications", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if self.scope["user"].is_staff:
            await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event["message"],
            'username': event["username"],
            'room': event["room"]
        }))
