# apps/accounts/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Принять соединение WebSocket

    def disconnect(self, close_code):
        pass  # Здесь можно закрывать соединение

    def receive(self, text_data):
        # Обработка полученного сообщения
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправка сообщения обратно клиенту
        self.send(text_data=json.dumps({
            'message': message
        }))
