"""
ASGI config for Visa4u project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.accounts.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Visa4u.settings')

# Приложение ASGI будет поддерживать HTTP и WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Обычные HTTP-запросы
    "websocket": AuthMiddlewareStack(  # WebSocket-соединения с авторизацией
        URLRouter(
            apps.accounts.routing.websocket_urlpatterns
        )
    ),
})

