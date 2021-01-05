from binance.websockets import BinanceSocketManager

def open_websocket(client):
    bm = BinanceSocketManager(client)
    
def get_depth_stream_str(symbol, depth=20, update_interval="100ms"):
    return f"{symbol.lower()}@depth@{depth}@{update_interval}"

def print_message(msg):
    print(f"message type: {msg['e']}")
    print(msg)
    