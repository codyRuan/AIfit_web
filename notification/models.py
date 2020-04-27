from django.db import models
from mongoengine import *
# Create your models here.

class Notification(Document):

    meta = {
        'collection': 'notification'
    }
    user_id = StringField()
    message_title = StringField()
    message_body = StringField()
    datetime = StringField()
    frm = StringField()