# chat/routing.py
from django.urls import re_path

from . import consumers
from . import example
websocket_urlpatterns = [
    re_path(r'wss/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'wss/ex/(?P<room_name>\w+)/$', example.Example),
]
