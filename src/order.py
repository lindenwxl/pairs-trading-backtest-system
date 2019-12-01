from position import Position
import config

class Order:
    def __init__(
        self,
        pair,
        spread_when_placed,
        long_position,
        short_position
    ):
        self.pair = pair
        self.spread_when_placed = spread_when_placed
        self.long_position = long_position
        self.short_position = short_position

    def initial_short_value_btc(self):
        return self.short_position.initial_value_btc

    def initial_long_value_btc(self):
        return self.long_position.initial_value_btc
