import datetime as dt
import os
import dateparser

from trading.database.utils import connect_to_db
from trading.database.data_point import DataPoint
from trading.websockets.binance.env import Env as BinanceEnv
from trading.websockets.snapshotter import Snapshotter

DB_NAME = "trading_data"
db = connect_to_db(DB_NAME)
DataPoint.objects.delete()

tickers = ["BNBBTC"]
streams = ["trade"]
binance_env = BinanceEnv(tickers, streams, max_trade_history=10)
snapshotter = Snapshotter(binance_env, snap_every=15, max_mongo_cache=1)

binance_env.start_stream()
snapshotter.start(print_saves=True)