import datetime as dt
import time
import os
import dateparser
from collections import deque
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.depthcache import DepthCacheManager

from trading.websockets.base_env import BaseEnv
from trading.websockets.binance import utils
from trading.database.data_point import DataPoint
class Env(BaseEnv):
    """
    This object controls all the 
    """
    def __init__(self, tickers, streams=["trade"], max_trade_history=5, max_lob_depth=10):
        """
        tickers: list
            a list of tickers corresponding to the trading pairs that we're watching
        streams: list
            a list of streams we're conencting to, excluding the depth one bc that's handled differently
        max_trade_history: int
            the numbers of recent trades to keep cached
            default: 5
        max_lob_depth: int
            the max depth for the limit book i.e. 20 means we record 20 bids and 20 asks 
            default: 10

        """
        super().__init__("binance_us", tickers)
        API_PUBLIC = os.environ.get("B_PUBLIC_KEY")
        API_SECRET = os.environ.get("B_SECRET_KEY")
        self.client = Client(API_PUBLIC, API_SECRET)
        self.tickers = tickers
        self.streams = streams
        self.max_trade_history = max_trade_history
        self.max_lob_depth = max_lob_depth
        self.data = {
            ticker.lower():{
                "trades": deque(maxlen=self.max_trade_history),
                "orderbook": None # not caching these for now
            }
            for ticker in self.tickers
        }
        self.dcms = {}
        self.socket_alive = False
        self.multiplex_strs = []
        
    def process_orderbook_message(self, msg):
        orderbook_doc = utils.process_orderbook_message(msg)
        self.data[msg.symbol.lower()]["orderbook"] = orderbook_doc
        
    def process_multiplex_message(self, msg):
        ticker, stream_type, data = utils.format_multiplex_message(msg)
        if stream_type == "trade":
            trade_doc = utils.process_trade_message(data)
            self.data[ticker]["trades"].append(trade_doc)
            
    def make_websocket(self):
        self.bsm = BinanceSocketManager(self.client)
        self.socket_alive = True
        
    def make_multiplex_stream_strs(self):
        """
        makes stream strings for each ticker for the 'trade' stream only
        """
        for ticker in self.tickers:
            for stream in self.streams:
                stream_str = f"{ticker.lower()}@{stream}"
                self.multiplex_strs.append(stream_str)
                
    def start_stream(self):
        if not self.socket_alive:
            self.make_websocket()
        
        if not self.multiplex_strs:
            self.make_multiplex_stream_strs()
            
        self.multiplex_conn_key = self.bsm.start_multiplex_socket(
            self.multiplex_strs, 
            self.process_multiplex_message
        )
        for ticker in self.tickers:
            # make this last (it starts bm underhood)
            dcm = DepthCacheManager(
                self.client, 
                ticker.upper(),
                self.process_orderbook_message,
                refresh_interval=1800,
                bm=self.bsm,
                limit=self.max_lob_depth
            )
            self.dcms[ticker] = dcm
        print(f"started stream for env: {self.exchange_name}")
        
    def save_env_snapshot(self):
        doc = DataPoint(data=self.data)
        self.mongo_cache.append(doc)
        
    def close_socket(self):
        self.bsm.close()
        self.socket_alive = False
        print(f"ended stream for env: {self.exchange_name}")
        
        
    