from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.contrib import messages
from datetime import datetime
import requests
import base64
import json
import uuid
from signup.models import User
# Create your views here.
def home(request):
    '''
    try:
        expire_time = request.session['expire_time']
    except:
        expire_time = "0"
    if datetime.now().strftime("%d/%m/%Y %H:%M:%S") >= expire_time:
       request.session.clear()
       messages.success(request,"please login again")
    '''
    return render(request, 'home.html')

def welcome(request):
   s = request.session.items()
   name = request.session['user_name']
   if datetime.now().strftime("%d/%m/%Y %H:%M:%S") >= request.session['expire_time']:
       request.session.clear()
       messages.success(request,"please login again")
   else:
        pass
      #messages.success(request,"welcome")
   return render(request, 'welcome.html', {"user_name":name})
        
   # return render(request, 'temp_home.html', {"user_id":  user_info['identifier'], "user_name": user_info['chinese-name']}) 

@api_view(['GET'])
def oauth_callback(request):
    code = None
    client_id = '#20200205015015-lZEQOJ3v'
    client_secret = 'CUdP9EYqmocWAxpQmArIBX3lz9hcOcHRSt3e18HKchkohjYXWHw0v9agMlRUadT2'
    try:
        code = request.GET["code"]
    except:
        error_description = request.GET["error_description"]
        return error_description
    b64_basic = base64.b64encode((client_id + ':' + client_secret).encode("utf-8")).decode("utf-8")
    response = requests.post('https://portal3g.ncu.edu.tw/oauth2/token',
                             json={"code": code, "redirect_uri": "https://ncufit.tk",
                                   "grant_type": "authorization_code"}, headers={"Authorization": "Basic " + b64_basic , "expires_in":"72000"})
    token_data = response.json()
    print(token_data)
    access_token_ = token_data['access_token']
    response = requests.get('https://portal3g.ncu.edu.tw/apis/oauth/v1/info',
                            headers={"Authorization": "Bearer " + access_token_ , "expires_in":"72000"})
    user_info = response.json()
    #print(user_info)
    #print(token_data)
    #print(user_info['identifier'])
    uid = str(uuid.uuid4())
    save_user(request,user_info['identifier'],user_info['chinese-name'])
    user = User(date_time=datetime.now())
    user.myid = user_info['identifier']
    user.name = str(user_info['chinese-name'])
    user.uuid = uid
    user.save()
    user_info.update({"uuid":uid})
    user_info.update({'chinese_name':str(user_info['chinese-name'])})
    return JsonResponse(user_info)
    #return HttpResponseRedirect('/oauth/welcome')
    #return render(request, 'temp_home.html', {"user_id":  user_info['identifier'], "user_name": user_info['chinese-name']})

def save_user(request,stuid, name):
    dt_string = (datetime.now()+timedelta(seconds=1800)).strftime("%d/%m/%Y %H:%M:%S")
    request.session['expire_time'] = dt_string
    request.session['student_id'] = stuid
    request.session['user_name'] = name
    
def get_user(request):
    pass

def logout(request):
    request.session.clear()
    messages.success(request,"logout successfully!")
    return render(request, 'logout.html')