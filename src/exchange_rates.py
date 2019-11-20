import requests
import numpy

class ExchangeRates:
    @classmethod
    def get_exchange_rates_from_candles(self, candles, pair):
        exchange_rates_A = [i[4] for i in candles[pair[0]]]
        exchange_rates_B = [i[4] for i in candles[pair[1]]]

        return [exchange_rates_A, exchange_rates_B]

    @classmethod
    def normalize(self, exchange_rates):
        return numpy.array(exchange_rates)/exchange_rates[0]

    @classmethod
    def from_candles(self, candles):
        exchange_rates = {}

        for asset, candle in candles.items():
            if not asset == 'GBPBTC':
                exchange_rates[asset] = candle[-1][4]

        return exchange_rates
