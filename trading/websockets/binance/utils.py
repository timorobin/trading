from operator import itemgetter
import dateparser

from trading.database.data_point import DataPoint

def get_depth_stream_str(symbol, depth=20, update_interval="1000ms"):
    return f"{symbol.lower()}@depth{depth}@{update_interval}"

def get_trade_stream_str(symbol):
    return f"{symbol.lower()}@trade"

def print_message(msg):
    print(msg)
    
def process_trade_message(msg):
    """
    description of data fields here:
        https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#trade-streams
    
    *note: msg comes in from multiplex stream, it will be in form of:
        {"stream": "stream_str", "data": dict of data}
    """
    data_field_mappings = {
        "t": "trade_id",
        "p": "price",
        "q": "quantity",
        "b": "buy_order_id",
        "a": "sell_order_id",
        "T": "trade_time",
        "m": "limit_buy"
    }
    data_getter=itemgetter(*data_field_mappings.keys())
    
    if "stream" in msg:
        msg = msg["data"]
    doc = {
        "source": "binance",
        "sub_source": "websocket_stream",
        "event_type": msg["e"],
        "event_time": dateparser.parse(str(msg["E"])),
        "symbol": msg["s"],
        "data": dict(zip(data_field_mappings.values(), data_getter(msg)))
    }
    doc["data"]["trade_time"] = dateparser.parse(str(msg["T"]))
    return DataPoint(**doc)
    
    
def process_lob_message(msg):
    """
    using depth cache manager object: 
        https://github.com/sammchardy/python-binance/blob/master/binance/depthcache.py
    """
    doc = {
        "source": "binance",
        "sub_source": "websocket_stream",
        "event_type": "lob_update",
        "event_time": dateparser.parse(str(msg.update_time)),
        "symbol": msg.symbol,
        "data": {
            "bids": msg.get_bids(),
            "asks": msg.get_asks()
        }
    }
    return DataPoint(**doc)