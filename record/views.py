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
from copy import deepcopy
# Create your views here.

@api_view(['post', 'GET'])
def api_history(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        print("id: {id}, uuid: {uuid}".format(id=my_id,uuid=my_uuid))

        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            rawData = Item.objects.filter(user_id=my_id)
            all_date_set = set()
            for data in rawData:
                all_date_set.add(data.date)
            new_date_list = list(all_date_set)
            new_date_list.sort(reverse=True)
            print(new_date_list)
            json_data = {}
            all_item = []
            tempItem = []
            for val in new_date_list:              
                dateData = Item.objects.filter(user_id=my_id,date=val)               
                for data in dateData:
                    tempItem.append({"item":data.item, "time":data.time, "group":data.group, "times":data.times, "total_time":data.total_time})                 
                all_item.append({"date":val,"data":deepcopy(tempItem)})
                tempItem.clear()               
            #json_data.update({"allOfItem":all_item})
            #json_data.update({"item":all_item})
            return Response(all_item)
    return Response("error")

def history(request):
    name = request.session['user_name']
    user_id = request.session['student_id']
    if datetime.now().strftime("%d/%m/%Y %H:%M:%S") >= request.session['expire_time']:
        request.session.clear()
        messages.success(request,"please login again")
    else:
        pass
    date = datetime.now().strftime("%Y") + '-' + datetime.now().strftime("%m") + '-' + datetime.now().strftime("%d")
    if request.method == 'POST':
        date = request.POST.get('date', "")
    return render(request, 'history.html', {"show_title": "運動紀錄", "items": Item.objects.filter(date=date, user_id=user_id), "tmp": date, "user_name": name})

@api_view(['POST', 'GET'])
def addwork(request):
    # if request.method == 'GET':
    #     item = request.GET['item']
    #     item = Item(item=item)
    #     item.save()
    #     times = request.GET['times']
    #     item.times = times
    #     time = datetime.now().strftime("%H") + ':' + datetime.now().strftime("%M")
    #     item.time = time
    #     date = datetime.now().strftime("%Y") + '-' + datetime.now().strftime("%m") + '-' + datetime.now().strftime("%d")
    #     item.date = date
    #     item.tag = 'tag'
    #     item.save()
    #     rets = {"item": item, 'times': times}
    #     retsj = json.dumps(rets)  # 返回json类型数据 {"source": "/mnt/source1/qin.txt", "target": "/mnt/target1/qin.txt"}
    #     return HttpResponse(retsj)
    if request.method == 'POST':
        item = request.POST.get('item')
        item = Item(item=item)
        item.user_id = request.session['student_id']
        group = request.POST.get("group")
        item.group = group
        item.save()
        times = request.POST.get("times")
        item.times = times
        time = datetime.now().strftime("%H") + ':' + datetime.now().strftime("%M")
        item.time = time
        date = datetime.now().strftime("%Y")+'-'+datetime.now().strftime("%m")+'-'+datetime.now().strftime("%d")
        item.date = date
        item.tag = 'tag'
        item.save()
        return HttpResponseRedirect('/record/history')
    else:
        return render(request, 'addwork.html')
