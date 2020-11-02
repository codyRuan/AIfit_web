from django.shortcuts import render, HttpResponseRedirect
#from django.http import HttpResponse
from datetime import datetime
from lineup.models import Line, QRCode_Record
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


# Create your views here.
def trigger(PD,MI):
    LO = Line.objects.filter(part=PD,user_id=MI)
    ws = websocket.create_connection('wss://ncufit.tk/wss/ex/mech1/', sslopt={"cert_reqs": ssl.CERT_NONE}, )
    uid = str(uuid.uuid4())
    user = User.objects.filter(myid=MI)
    QRCode_Record(user_id=MI, part=PD, qrcode=uid).save()
    for usr in user: 
        usr.update(set__qrcode=uid)
    
            
    for LOdata in LO:
        for i in range(50, -1, -1):
            if Line.objects.filter(part=PD,user_id=MI).first().countdown != -1:
                LOdata.update(set__countdown=int(i))
                print(Line.objects.filter(part=PD,user_id=MI).first().countdown)
                Q_T = {"uid":uid,"timer":i}
                data = {"message": "QRcode_raw&timer", "part":Q_T, "sid":MI}
                ws.send(json.dumps(data))
                result = ws.recv()
                sleep(1)
        if Line.objects.filter(part=PD,user_id=MI).first().countdown != -1:   
            for new in Line.objects.filter(part=LOdata.part):
                if new.precedence > 1:
                    new.update(set__precedence=new.precedence-1)
            LOdata.delete()
            userData = User.objects.filter(myid=MI)[0]
            title = "Time out!"
            body = "dear {name}, you have been removed from the {device} ಥ_ಥ!".format(
                            name=userData.name, device=PD)
            postNotificationToSingleUser(MI, title, body, "NCUfit LineUp SYS")
    ws.close()

    # do something else here.
def caltime(sec):
    timeinhms = ""
    rt = sec
    if rt >= 3600:
        timeinhms = timeinhms + str(rt//3600) + "h"
        rt = rt % 3600
    if rt >= 60 :
        timeinhms = timeinhms + str(rt//60) + "m"
        rt = rt % 60
    timeinhms += str(rt) + "s"
    return timeinhms

partlist=["深蹲","機械","臥推","上胸","硬舉","啞鈴"] 
@api_view(['post', 'GET'])
def join(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        this_part = Line.objects.filter(part=received_json_data['part'])
        part_to_line_up = Line(part=received_json_data['part'],user_id=my_id,precedence=this_part.count()+1,countdown=-2)
        print(part_to_line_up)
        
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid                
        if Line.objects.filter(part=received_json_data['part'],user_id=my_id).count() > 0:
            return Response({"message":"You are already in line"})
        elif User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            part_to_line_up.save()
            return Response({"message":"success"})
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
            total_time = 0
            for tp in Line.objects(part=received_json_data['part'],user_id=my_id):
                this_part_precedence = tp.precedence
                now = datetime.now()
                last = tp.time
                total_time = caltime((now-last).seconds)
            for new in this_part:
                if new.precedence > this_part_precedence:
                    new.update(set__precedence=new.precedence-1)
             
            Line.objects(part=received_json_data['part'],user_id=my_id).delete()
            this_training = Counting.objects.filter(part=received_json_data['part'], user_id=my_id,status = 0)
            total_times = 0
            total_set = this_training.count()
            for train in this_training:
                total_times = total_times + train.times
            this_training.delete()
            Counting.objects.filter(part=received_json_data['part']).delete()
            # websocket
            ws = websocket.create_connection('wss://ncufit.tk/wss/ex/mech1/', sslopt={"cert_reqs": ssl.CERT_NONE}, )
            data = {"message": "done", "part":received_json_data['part'], "sid":my_id}
            ws.send(json.dumps(data))
            result = ws.recv()
            ws.close()
            # socket end
            try:
                gup = str(total_set)
                tms = str(total_times)
                if gup == '0' or tms == '0':
                    return Response({"message":"finished training"})
                time = datetime.now().strftime("%H") + ':' + datetime.now().strftime("%M")
                date = datetime.now().strftime("%Y")+'-'+datetime.now().strftime("%m")+'-'+datetime.now().strftime("%d")
                saveItem = Item(item=received_json_data['part'], group=gup, times=tms, user_id=my_id, time=time, date=date,total_time=str(total_time))
                saveItem.save()
                return Response({"message":"End"})
            except:
                pass           
            return Response({"message":"did not save"})
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
                qstring = "排隊"
                countdowntime = -1
                this_part_precedence = 0
                for tp in Line.objects(part=partdata,user_id=my_id):
                    this_part_precedence = tp.precedence
                if Line.objects.filter(part=partdata,user_id=my_id).count() > 0:
                    if this_part_precedence == 1:
                        countdowntime = Line.objects.filter(part=partdata,user_id=my_id).first().countdown
                        lineData = Line.objects.filter(part=partdata,user_id=my_id)[0]
                        userData = User.objects.filter(myid=my_id)[0]
                        if countdowntime == -1:
                            qstring = "開始!"
                        else:
                            qstring = "到你了!"
                            if lineData.notification == False:
                                thread = threading.Thread(target=trigger, args = (partdata,my_id))
                                thread.daemon = True
                                thread.start()
                                title = "Your Turn!!"
                                body = "dear {name}, is your time to enjoy the {device}!".format(
                                        name=userData.name, device=partdata)
                                postNotificationToSingleUser(my_id, title, body, "NCUfit LineUp SYS")
                                lineData.update(notification=True)
                    else :
                        countdowntime = -1
                        qstring = "等待{x}人".format(x=this_part_precedence-1)
                all_item.append({"title": partdata,"data": [{ "precedence":this_part_precedence, "item": partdata, "amount": tmp, "user_qstatus":qstring, "countdown":str(countdowntime) }]})

            return Response(all_item)
    return Response("error")
@api_view(['post', 'GET'])
def StartWorkout(request):
    if request.method == 'POST':
        
        received_json_data=json.loads(request.body)
        qrcd = received_json_data['qrcode']
        qrcd = QRCode_Record.objects.filter(qrcode=received_json_data['qrcode']).first()
        # my_uuid = received_json_data['uuid']
        # raw_QRcode = received_json_data['QRcode']
        # my_id = received_json_data['user_id']
        # this_part = Line.objects.filter(part=received_json_data['part'])
        # print(my_id)
        # print(received_json_data['part'])
        # l = User.objects.filter(myid=my_id).count()
        # if l != 0:
            # latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid                            
        # if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid and Line.objects.filter(part=received_json_data['part'],user_id=my_id).count() > 0:
        if Line.objects.filter(part=qrcd.part,user_id=qrcd.user_id).count() > 0:
            LO = Line.objects.filter(part=qrcd.part,user_id=qrcd.user_id)
            for LOdata in LO:
                LOdata.update(set__countdown=-1)
                LOdata.update(set__time=datetime.now())
            # websocket
            ws = websocket.create_connection('wss://ncufit.tk/wss/ex/mech1/', sslopt={"cert_reqs": ssl.CERT_NONE}, )
            data = {"message": "start_workout", "part":qrcd.part, "sid":qrcd.user_id}
            ws.send(json.dumps(data))
            result = ws.recv()
            ws.close()
            # socket end
            return Response({"message":"start"})
    return Response("error")
    
@api_view(['post', 'GET'])
def GetTimer(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid                            
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid and Line.objects.filter(part=received_json_data['part'],user_id=my_id).count() > 0:
            tmp = Line.objects.filter(part=received_json_data['part'],user_id=my_id).first().countdown
            return Response({"message":str(tmp)})
    return Response("error")
    
@api_view(['post', 'GET'])
def forvideo(request):
    if request.method == 'POST':
    # received_json_data=json.loads(request.body)
    # ws = websocket.create_connection('wss://ncufit.tk/wss/ex/456/', sslopt={"cert_reqs": ssl.CERT_NONE}, )
    # print("Sending 'Hello, World'...")
    # data = received_json_data
    # ws.send(json.dumps(data))
    # print("Sent")
    # print("Receiving...")
    # result = ws.recv()
    # print("Received '%s'" % result)
    # ws.close()
    # my_id = received_json_data['user_id']
        # this_part = Line.objects.filter(part=received_json_data['part'])
        # part_to_line_up = Line(part=received_json_data['part'],user_id=my_id,precedence=this_part.count()+1)
        # print(part_to_line_up)
        # part_to_line_up.save()
        return Response({"message":"success"})
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
        if a == "Q": adddata('a')
        if b == "Q": adddata('b')
        if c == "Q": adddata('c')
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