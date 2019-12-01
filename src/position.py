import config

class Position:
    def __init__(self, asset, volume, exchange_rate):
        self.asset = asset
        self.volume = volume
        self.exchange_rate = exchange_rate
        self.initial_value_btc = config.btc_order_volume
