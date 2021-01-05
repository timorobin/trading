import os, datetime as dt, dateparser
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from binance.client import Client


def get_closes(client, symbol, interval, timedelta, d1=None):
    
    if d1 is None:
        d1 = dt.datetime.now(dt.timezone.utc)
    assert d1.tzinfo == dt.timezone.utc, "must use utc timezone dates"
    d0 = d1 - timedelta
    start_str = dt.datetime.strftime(d0, "%c")
    res =  client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_str)
#     return res, symbol, interval, start_str, d0
    (
        t0, o, h, 
        l, c, v, 
        t1, quote_asset_vol, num_trades, 
        tbb_vol, tbq_vol, _
    ) = zip(*res)
    df = pd.DataFrame(
        data=np.array([t0, o, h, l, c, v, t1, quote_asset_vol, num_trades, tbb_vol, tbq_vol]).T, 
        columns=["t0", "o", "h", "l", "c", "v", "t1", "quote_asset_vol", "num_trades", "tbb_vol", "tbq_vol"]
    )
    
    date_cols = ["t0", "t1"]
    float_cols = ["o", "h", "l", "c", "v", "quote_asset_vol", "tbb_vol", "tbq_vol"]
    int_cols = ["num_trades"]
    df["t0"] = df["t0"].apply(dateparser.parse)
    df["t1"] = df["t1"].apply(dateparser.parse)
    
    df[float_cols] = df[float_cols].astype(float)
    df[int_cols] = df[int_cols].astype(int)
    return df[["t1", "c"]]

def get_log_returns(returns):
    return np.log(returns[1:]/returns[:-1])