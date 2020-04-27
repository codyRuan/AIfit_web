from django.db import models
from mongoengine import *
# Create your models here.

class Item(Document):

    meta = {
        'collection': 'workout'
    }
    user_id = StringField()
    group = StringField()
    item = StringField()
    times = StringField()
    date = StringField()
    time = StringField()