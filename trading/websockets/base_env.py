class BaseEnv:
    """
    this is the base class for all exchange specific environments
    """
    def __init__(self, exchange_name, tickers):
        self.exchange_name = exchange_name
        self.tickers = tickers