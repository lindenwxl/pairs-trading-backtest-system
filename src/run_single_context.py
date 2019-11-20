from bot import Bot
from candles import Candles

candles = Candles.get_all(
    1.0,
    '1h'
)

Bot('1h', 1.0, 0.00005, 0.575, 72, candles)
