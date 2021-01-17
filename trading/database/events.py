import datetime as dt
from mongoengine import *
from uuid import uuid4

class Trade(EmbeddedDocument):
    guid = StringField(default=uuid4().hex)
    trade_id = StringField()
    price = FloatField()
    quantity = FloatField()
    buy_order_id = StringField()
    sell_order_id = StringField()
    trade_time = DateTimeField()
    is_limit_buy = BooleanField()
    
class LimitOrder(EmbeddedDocument):
    quantity = FloatField()
    price = FloatField()
    
class OrderBook(EmbeddedDocument):
    guid = StringField(default=uuid4().hex)
    bids = ListField(LimitOrder)
    asks = ListField(LimitOrder)
    
