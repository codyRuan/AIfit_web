import datetime
from mongoengine import Document, fields, DateTimeField


class HCSR04(Document):
    distance = fields.IntField(required=True)
    times = fields.IntField(required=True)
    rate = fields.IntField(required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

# Create your models here.
