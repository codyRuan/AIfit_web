from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from datetime import datetime
import json
from record.models import Item
from signup.models import User

# Create your views here.

@api_view(['post', 'GET'])
def checklogin(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        print(received_json_data['user_id'])
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        l = User.objects.filter(myid=my_id).count()
        print(my_id)
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l - 1].uuid
            print(latest_uuid)
            print(my_uuid)
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            print(my_id)
            json_data = {'code': 300}
            print(json_data)
            return Response(json_data)
        else:
            return Response({'code': 301})
    return Response("error")

