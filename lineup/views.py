from django.shortcuts import render, HttpResponseRedirect
#from django.http import HttpResponse
from datetime import datetime
from lineup.models import Line
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

partlist=["臥推","肩推"] 
@api_view(['post', 'GET'])
def join(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        this_part = Line.objects.filter(part=received_json_data['part'])
        part_to_line_up = Line(part=received_json_data['part'],user_id=my_id,precedence=this_part.count()+1)
        print(part_to_line_up)
        
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid                
        if Line.objects.filter(part=received_json_data['part'],user_id=my_id).count() > 0:
            return Response({"message":"你已經在列隊中"})
        elif User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            part_to_line_up.save()
            return Response({"message":"排隊成功"})
    return Response("error")
@api_view(['post', 'GET'])
def leave(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        this_part = Line.objects.filter(part=received_json_data['part'])
        
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid                            
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid and Line.objects.filter(part=received_json_data['part'],user_id=my_id).count() > 0:
            this_part_precedence = 0
            for tp in Line.objects(part=received_json_data['part'],user_id=my_id):
                this_part_precedence = tp.precedence
            for new in this_part:
                if new.precedence > this_part_precedence:
                    new.update(set__precedence=new.precedence-1)

            Line.objects(part=received_json_data['part'],user_id=my_id).delete()
            
            return Response({"message":"結束排隊"})
    return Response("error")
@api_view(['post', 'GET'])
def getQstatus(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        l = User.objects.filter(myid=my_id).count()
        
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            all_item = []
            for partdata in partlist:
                tmp = Line.objects.filter(part=partdata).count()
                qstring = "排隊!"
                this_part_precedence = 0
                for tp in Line.objects(part=partdata,user_id=my_id):
                    this_part_precedence = tp.precedence
                if Line.objects.filter(part=partdata,user_id=my_id).count() > 0:
                    if this_part_precedence == 1:
                        qstring = "輪到你了!"
                        lineData = Line.objects.filter(part=partdata,user_id=my_id)[0]
                        if lineData.notification == False:
                            postNotificationToSingleUser(my_id, partdata)
                            lineData.update(notification=True)
                    else :
                        qstring = "已排隊"
                all_item.append({"title": partdata,"data": [{ "precedence":this_part_precedence, "item": partdata, "amount": tmp, "user_qstatus":qstring }]})

            return Response(all_item)
    return Response("error")

def SelfQueuing(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        l = User.objects.filter(myid=my_id).count()
        partlist=["臥推","肩推"] 
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            for tp in Line.objects(part=partdata,user_id=my_id):
                    print(tp.precedence)
            return Response({"test":"123"})
    return Response("error")
def lineup(request):
    a = len(Line.objects.filter(item='a'))
    b = len(Line.objects.filter(item='b'))
    c = len(Line.objects.filter(item='c'))
    date = datetime.now().strftime("%Y") + '-' + datetime.now().strftime("%m") + '-' + datetime.now().strftime("%d")
    if request.method == 'POST':
        a = request.POST.get('line_a', "")
        b = request.POST.get('line_b', "")
        c = request.POST.get('line_c', "")
        if a == "我要排隊": adddata('a')
        if b == "我要排隊": adddata('b')
        if c == "我要排隊": adddata('c')
        a = len(Line.objects.filter(item='a'))
        b = len(Line.objects.filter(item='b'))
        c = len(Line.objects.filter(item='c'))
    return render(request, 'lineup.html', {"a": a, "b": b, "c": c, "user_name": request.session["user_name"]})

def adddata(item):
    line = Line(item=item)
    line.save()
    time = datetime.now().strftime("%H") + ':' + datetime.now().strftime("%M")
    line.time = time
    line.save()