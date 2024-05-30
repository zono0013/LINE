from django.urls import re_path

from . import consumers

# WebSocketConsumerは.as_asgi()で呼び出せる。
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)', consumers.ChatConsumer.as_asgi()),
]