from django.db import models
from mongoengine import *
import datetime

# Create your models here.
class postimage(Document):
    meta = {
        'collection': 'img'
    }
    user_id = StringField()
    img = ImageField()
    date_add = DateTimeField(default=datetime.datetime.utcnow)