import datetime as dt
from binance.websockets import BinanceSocketManager
from binance.depthcache import DepthCacheManager
from mongoengine import connect

from trading.database.data_point import DataPoint
from trading.websockets.binance import utils

class Listener:
    """
    this object sets up binance websocket connections and records
    whatever it finds in mongo
    """
    def __init__(self, binance_client, symbol, db_name):
        self.binance_client = binance_client
        self.symbol = symbol
        connect(db_name)
        self.doc_container = []
        self.max_container_size = 1000
        
    def process_trade_message(self, msg):
        doc = utils.process_trade_message(msg)
        self.doc_container.append(doc)
        if len(self.doc_container) > self.max_container_size:
            self.empty_doc_container()

    def process_dcm_message(self, msg):
        self.lob = msg
        doc = utils.process_lob_message(msg)
        self.doc_container.append(doc)
        if len(self.doc_container) > self.max_container_size:
            self.empty_doc_container()
            
    def empty_doc_container(self):
        DataPoint.objects.insert(self.doc_container)
        self.doc_container = []
        t = dt.datetime.now().__str__()
        print(f"{self.symbol} batch sent to mongo at {t}")
        
    def make_websocket(self):
        self.bm = BinanceSocketManager(self.binance_client)
#         self.conn_key = self.bm.start_trade_socket(
#             self.symbol, self.process_trade_message
#         )
    def start_stream(self):
        # make this last (it starts bm underhood)
        self.dcm = DepthCacheManager(
            self.binance_client, 
            self.symbol, 
            self.process_dcm_message,
            refresh_interval=1800,
            bm=self.bm,
            limit=20
        )
        
    def close_socket(self):
        self.bm.stop_socket(self.conn_key)
        self.bm.close()
        self.dcm.close(close_socket=True)
        
    