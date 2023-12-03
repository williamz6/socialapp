from django.urls import path
from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from .consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
]

