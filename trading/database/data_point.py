import datetime as dt
from mongoengine import *

class DataPoint(Document):
    meta = {
        "collection": "datapoints",
        "indexes": ["timestamp"]
    }
    