from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import json
import requests
from notification.models import Notification
from signup.models import User
# Create your views here.


@api_view(['post', 'GET'])
def GetMessage(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        print("id: {id}, uuid: {uuid}".format(id=my_id, uuid=my_uuid))
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            rawNFT = Notification.objects.filter(user_id=my_id)
            temp_list = []
            for nfc in rawNFT:
                temp_list.append(
                    {"datetime": nfc.datetime, "title": nfc.message_title, "body": nfc.message_body})

            return Response(temp_list)
        return Response("error")


@api_view(['post', 'GET'])
def deletMessage(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        my_uuid = received_json_data['uuid']
        my_id = received_json_data['user_id']
        dt = received_json_data['datetime']
        l = User.objects.filter(myid=my_id).count()
        if l != 0:
            latest_uuid = User.objects.filter(myid=my_id)[l-1].uuid
        if User.objects.filter(myid=my_id, uuid=my_uuid).count() > 0 and my_uuid == latest_uuid:
            dltMessage = Notification.objects.filter(user_id=my_id,datetime=dt).delete()
            return Response("you have delete the message on date :{}".format(dt))
        return Response("fail to delete the message")

def postNotificationToSingleUser(user_id, item):
    userData = User.objects.filter(myid=user_id)[0]
    token = userData.device_token
    print(token)
    Auth_key = "key=AAAAZMklHac:APA91bG8eVOvCmh0NGBhGZD8vA98hqRRmT4MypWAP7c6CsSGgjTnhy3ksmh12_7_aW58jFIaaBJaJKvCVwnTZewFqok8E2eVGc4DgEvSt71lC30iyKOwPEUpnyCEtimzxJxMrhkNozRZ"
    title = "Your Turn!!"
    body = "dear {name}, is your time to enjoy the {device}!".format(
        name=userData.name, device=item)
    Datetime = datetime.now().strftime("%Y/%m/%d   %H:%M:%S")
    nfc = Notification(user_id=user_id, message_title=title, message_body=body)
    nfc.datetime = Datetime
    nfc.save()
    response = requests.post('https://fcm.googleapis.com/fcm/send',
                             json={"to": str(token),
                                   "notification": {"sound":"default","title": title, "body": body}
                                   }, headers={"Content-Type": "application/json", "Authorization": Auth_key})

@api_view(['post', 'GET'])
def postNotificationToAllUser(request):
    System_key = "key=AAAAZMklHac:APA91bG8eVOvCmh0NGBhGZD8vA98hqRRmT4MypWAP7c6CsSGgjTnhy3ksmh12_7_aW58jFIaaBJaJKvCVwnTZewFqok8E2eVGc4DgEvSt71lC30iyKOwPEUpnyCEtimzxJxMrhkNozRZ"
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        Auth_key = received_json_data['Auth_key']
        title = received_json_data['title']
        body = received_json_data['body']
        if Auth_key == System_key:
            allUser = User.objects.all()
            deviceToken = {}
            for user in allUser:
                deviceToken.update({user.myid:user.device_token})
            for id in deviceToken:
                Datetime = datetime.now().strftime("%Y/%m/%d   %H:%M:%S")
                nfc = Notification(user_id=id, message_title=title, message_body=body)
                nfc.datetime = Datetime
                nfc.save()
                token = deviceToken[id]
                response = requests.post('https://fcm.googleapis.com/fcm/send',
                             json={"to": str(token),
                                   "notification": {"sound":"default","title": title, "body": body}
                                   }, headers={"Content-Type": "application/json", "Authorization": Auth_key})
            return Response("the message was sent to {num} {p}".format(num=str(len(deviceToken)),p=("person" if len(deviceToken) == 1 else "people")))
        else:
            return Response("AuthKey invalid")
    return Response("failed request")

@api_view(['post', 'GET'])
def GetDeviceToken(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        device_token = received_json_data['token']
        my_id = received_json_data['user_id']
        print(device_token)
        newUser = User.objects.filter(myid=my_id).update(
            device_token=device_token)  # update user's device token
        return Response("update device token successfully!")

    return Response("error")
