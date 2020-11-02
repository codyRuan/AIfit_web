from django.db import models
from mongoengine import *
# Create your models here.

class User(Document):

    meta = {
        'collection': 'login_record'
    }
    date_time = DateTimeField()
    myid = StringField()
    name = StringField()
    uuid = StringField()
    device_token = StringField()
    qrcode = StringField()
    