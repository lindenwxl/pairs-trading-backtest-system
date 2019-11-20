from position import Position

class Order:
    def __init__(self, pair, spread_when_placed, long_position, short_position):
        self.pair = pair
        self.spread_when_placed = spread_when_placed
        self.long_position = long_position
        self.short_position = short_position
