from django.db import models
from mongoengine import *
import datetime
import pytz
# Create your models here.

class Line(Document):

    meta = {
        'collection': 'lineup'
    }
    time = DateTimeField(default=pytz.timezone('Asia/Taipei').localize(datetime.datetime.now()))
    user_id = StringField()
    item = StringField()
    precedence = IntField()
    part = StringField()
    notification = BooleanField(default=False)