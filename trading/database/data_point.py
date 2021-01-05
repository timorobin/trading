import datetime as dt
from mongoengine import *
from uuid import uuid4

class DataPoint(Document):
    meta = {
        "collection": "datapoints",
        "indexes": ["guid", "source", "event_time", "event_type", "symbol"]
    }
    guid = StringField(default=uuid4().hex)
    source = StringField(required=True)
    sub_source = StringField()
    event_type = StringField(required=True)
    symbol = StringField(required=True)
    event_time = DateTimeField(required=True)
    received_at = DateTimeField(default=dt.datetime.now)
    data = DictField()
    
    