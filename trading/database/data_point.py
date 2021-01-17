import datetime as dt
from mongoengine import *
from uuid import uuid4

class DataPoint(Document):
    meta = {
        "collection": "datapoints",
        "indexes": ["guid", "timestamp"]
    } 
    guid = StringField(default=uuid4().hex)
    timestamp = ComplexDateTimeField(default=dt.datetime.utcnow)
    data = DictField()