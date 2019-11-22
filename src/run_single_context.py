from bot import Bot
from candles import Candles

candles = Candles.get_all(
    168,
    '7D'
)

Bot('7D', 168, 0.00005, 0.575, 10, candles)
