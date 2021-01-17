import datetime as dt
import os
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import dateparser

import math
import matplotlib.pyplot as plt
from binance.client import Client

from trading.websockets.binance import listener

API_PUBLIC = os.environ.get("B_PUBLIC_KEY")
API_SECRET = os.environ.get("B_SECRET_KEY")
binance_client = Client(API_PUBLIC, API_SECRET)

symbols = ["ADABTC", "LINKBTC", "ETHBTC", "BNBBTC"]
db_name = "trading_data"

listeners = [
    listener.Listener(binance_client, symbol, db_name)
    for symbol in symbols
]
for l in listeners:
    l.make_websocket()
    l.start_stream()