from operator import itemgetter
import dateparser

from trading.database.events import Trade, OrderBook, LimitOrder
from trading.database.data_point import DataPoint

def get_depth_stream_str(symbol, depth=20, update_interval="1000ms"):
    return f"{symbol.lower()}@depth{depth}@{update_interval}"

def get_trade_stream_str(symbol):
    return f"{symbol.lower()}@trade"

def print_message(msg):
    print(msg)

def format_multiplex_message(msg):
    stream, data = msg.values()
    ticker, stream_type = stream.split("@")
    return ticker, stream_type, data

def process_trade_message(msg):
    """
    description of data fields here:
        https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#trade-streams
    """
    data_field_mappings = {
        "t": "trade_id",
        "p": "price",
        "q": "quantity",
        "b": "buy_order_id",
        "a": "sell_order_id",
        "T": "trade_time",
        "m": "is_limit_buy"
    }
    data_getter=itemgetter(*data_field_mappings.keys())
    data = dict(zip(data_field_mappings.values(), data_getter(msg)))
    trade_doc = Trade(**data)
    return trade_doc
    
def process_orderbook_message(msg):
    """
    using depth cache manager object: 
        https://github.com/sammchardy/python-binance/blob/master/binance/depthcache.py
    """
    bids = [LimitOrder(price=bid[0], quantity=bid[1]) for bid in msg.get_bids()]
    asks = [LimitOrder(price=ask[0], quantity=ask[1]) for ask in msg.get_asks()]
    
    orderbook_doc = OrderBook(bids=bids, asks=asks)    
    return orderbook_doc

#     doc = {
#         "source": "binance",
#         "sub_source": "websocket_stream",
#         "event_type": msg["e"],
#         "event_time": dateparser.parse(str(msg["E"])),
#         "symbol": msg["s"],
#         "data": dict(zip(data_field_mappings.values(), data_getter(msg)))
#     }


#     doc = {
#         "source": "binance",
#         "sub_source": "websocket_stream",
#         "event_type": "lob_update",
#         "event_time": dateparser.parse(str(msg.update_time)),
#         "symbol": msg.symbol,
#         "data": {
#             "bids": msg.get_bids(),
#             "asks": msg.get_asks()
#         }
#     }