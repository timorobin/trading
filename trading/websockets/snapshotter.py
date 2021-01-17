import datetime as dt
import time
import dateparser
from trading.database.data_point import DataPoint

class MongoCache:
    """
    simple mongo cache 
    """
    def __init__(self, empty_every):
        self.empty_every = empty_every
        self.cache = []
        
    def __len__(self):
        return len(self.cache)
    
    def append(self, item, exchange_name=None, ti=None):
        self.cache.append(item)
        if len(self) >= self.empty_every:
            DataPoint.objects.insert(self.cache)
            self.cache = []
            print(f"saved {len(self)} datapoints from {exchange_name} at: {dateparser.parse(str(ti))}")

class Snapshotter:
    """
    observes and saves environement data as a mongo doc every so often
    """
    def __init__(self, env, snap_every=30, max_mongo_cache=1):
        """
        Args:
            env: exchange environment class
                the environment we're snapshotting. Should started prior to initializing the object
            snap_every: int
                the number of seconds to wait until taking another snapshot of the data. 
                If zero, snaps as fast as possible
                default: 30
            max_mongo_cache: int
                the max size of the mongo cache before we send it to mongo.
                default: 1
        """
        self.env = env
        self.snap_every = snap_every
        self.max_mongo_cache = max_mongo_cache
        self.cache = MongoCache(self.max_mongo_cache)
        
    def start(self):
        print(f"snapshotter started for env: {self.env.exchange_name}")
        t0 = time.time() # init time
        while self.env.socket_alive:
            ti = time.time()
            if ti - t0 > self.snap_every:
                snap = DataPoint(data=self.env.data)
                self.cache.append(snap, self.env.exchange_name, ti)
                t0 = ti

                
        print(f"env: {self.env.exchange_name} closed. snapshotter closing too")