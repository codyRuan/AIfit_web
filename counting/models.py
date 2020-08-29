from django.db import models
from mongoengine import *
import datetime
import pytz
# Create your models here.

class Counting(Document):

    meta = {
        'collection': 'counting'
    }
    time = DateTimeField(default=pytz.timezone('Asia/Taipei').localize(datetime.datetime.now()))
    user_id = StringField()
    set_num = IntField()
    times = IntField()
    part = StringField()
    status = IntField() #正在做(1)/已做完(0)