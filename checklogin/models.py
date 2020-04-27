from django.db import models
from mongoengine import *
import datetime


# Create your models here.
class LoginState(Document):
    meta = {
        'collection': 'Last_used_time'
    }
    user_id = StringField()
    last = DateTimeField(default=datetime.datetime.utcnow)

