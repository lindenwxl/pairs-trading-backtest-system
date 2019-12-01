from bot import Bot
from candles import Candles

candles = Candles.get_all(
    6,
    '6h'
)

Bot('6h', 6, 0.00005, 0.575, 500, candles)
