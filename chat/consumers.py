from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from lineup.models import Line
from counting.models import Counting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from record.models import Item
from signup.models import User
from notification.views import postNotificationToSingleUser
from copy import deepcopy
import threading
from time import sleep
import json 
from channels.generic.websocket import AsyncWebsocketConsumer 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        part = text_data_json['part']
        sid = text_data_json['sid']
        tmp = User.objects.filter(myid='106502521').count()
        print(tmp)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'part':part,
                'sid':sid
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        part = event['part']
        sid = event['sid']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'part':part,
            'sid':sid
        }))
        
        
        
class Example(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # part = text_data_json['part']
        # sid = text_data_json['sid']
        # # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'message',
                'part':'part',
                'sid':'sid'
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        part = event['part']
        sid = event['sid']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'part':part,
            'sid':sid
        }))

