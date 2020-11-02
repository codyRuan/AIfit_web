from django.shortcuts import render, HttpResponseRedirect
#from django.http import HttpResponse
from datetime import datetime
from lineup.models import Line
from counting.models import Counting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
import json
from record.models import Item
from signup.models import User
from notification.views import postNotificationToSingleUser
from copy import deepcopy
import threading
from time import sleep
import uuid
import websocket
import ssl
try:
    import thread
except ImportError:
    import _thread as thread
import time
@api_view(['post', 'GET'])
def qws(request):
    if request.method == 'POST':
        return Response({"message":"123"})
    return Response("error")
