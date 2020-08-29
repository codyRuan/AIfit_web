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
# Create your views here.


@api_view(['post', 'GET'])
def getcurrentset(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        l = User.objects.filter(myid=my_id).count()
        
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            this_training_details = []
            this_training = Counting.objects.filter(part=received_json_data['part'], user_id=my_id,status=0)
            current_training = Counting.objects.filter(part=received_json_data['part'], user_id=my_id,status=1).first()
            total_times = 0
            total_set = this_training.count()
            for train in this_training:
                total_times = total_times + train.times
                this_training_details.append({"group":train.set_num,"times":train.times})
            try:
                rspdata = {"group":current_training.set_num,"times":current_training.times, "all":this_training_details}
            except:
                rspdata = {"group":total_set,"times":total_times, "all":this_training_details}
            return Response(rspdata)
    return Response("error")
        
    
    
    
@api_view(['post', 'GET'])
def setcount(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        this_user = Counting.objects.filter(part=received_json_data['part'], user_id=received_json_data['user_id'], status = 0)
        new_set = Counting(part=received_json_data['part'], user_id=received_json_data['user_id'], times=received_json_data['times'], set_num=this_user.count()+1, status = received_json_data['status'])
        if received_json_data['status'] == 0:
            if new_set.times != 0:
                new_set.save()
            return Response({'set':str(this_user.count()),'times':str(new_set.times)})
        elif received_json_data['status'] == 1:
            
            try:
                current_record = Counting.objects.filter(part=received_json_data['part'], user_id=received_json_data['user_id'], status = 1).first().delete()
            except:
                pass
            new_set.save()
            return Response({'set':str(this_user.count()+1),'times':str(received_json_data['times'])})
            
    return Response("error") 


@api_view(['post', 'GET'])
def detectuser(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        try:
            this_item_first_user = Line.objects.filter(part=received_json_data['item']).first()
            if this_item_first_user.precedence == 1 and this_item_first_user.countdown == -1:
                return Response({'part':str(received_json_data['item']), 'user_id':str(this_item_first_user.user_id)})
        except:
                pass
    return Response({'user_id':''})
    
    
@api_view(['post', 'GET'])
def fortest(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_id = received_json_data['user_id']
        which_part = received_json_data['part']
        print(received_json_data)
        
        this_training_details = []
        this_training = Counting.objects.filter(part=which_part, user_id=my_id)
        total_times = 0
        total_set = this_training.count()
        print(total_set)
        for train in this_training:
            total_times = total_times + train.times
            this_training_details.append({"group":train.set_num,"times":train.times})
        rspdata = {"group":total_set,"times":total_times, "all":this_training_details}
        return Response(rspdata)
    return Response("error")