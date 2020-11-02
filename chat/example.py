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

correct = False
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
        message = text_data_json['message']
        part = ''
        sid = ''
        if message == "QRcode":
            rcv_qrcode = text_data_json['part']
            id = text_data_json['sid']
            part = rcv_qrcode
            sid = id
            # crt_qrcode = User.objects.filter(myid=my_id)[0].qrcode
            # if rcv_qrcode == crt_qrcode:
            #     correct = True
        elif message == "QRcode_raw&timer":
            rcv_qrcode = text_data_json['part']
            id = text_data_json['sid']
            part = rcv_qrcode
            sid = id
        elif message == 'timer':
            time = text_data_json['part']
            id = text_data_json['sid']
            part = time
            sid = id
        elif message == 'start_workout':
            id = text_data_json['sid']
            part = {"part":text_data_json['part'], "countdown":-9}
            sid = id
        elif message == 'judgePose':
            part = text_data_json['part']
            id = text_data_json['sid']
            sid = id
        # # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'part':part,
                'sid':sid,
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
