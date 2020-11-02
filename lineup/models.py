from django.db import models
from mongoengine import *
import datetime
import pytz
# Create your models here.

class Line(Document):

    meta = {
        'collection': 'lineup'
    }
    time = DateTimeField(default=datetime.datetime.now())
    user_id = StringField()
    item = StringField()
    precedence = IntField()
    part = StringField()
    countdown = IntField()
    notification = BooleanField(default=False)
    gp = StringField()
    ts = StringField()
    verified = IntField(default=0)

class QRCode_Record(Document):

    meta = {
        'collection': 'qrcode'
    }
    time = DateTimeField(default=datetime.datetime.now())
    part = StringField()
    user_id = StringField()
    qrcode = StringField()
    