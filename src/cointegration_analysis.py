import statsmodels.tsa.stattools as ts
import config
from cointegrated_pair import CointegratedPair
from exchange_rates import ExchangeRates
import helpers
import pandas as pd

class CointegrationAnalysis:
    def __init__(self, pair, exchange_rates, candles):
        self.pair = pair
        self.exchange_rates = exchange_rates
        self.candles = candles
        self.get_asset_exchange_rates()
        self.analyse()

    def analyse(self):
        self.analysis = ts.coint(
            ExchangeRates.normalize(self.exchange_rates_A),
            ExchangeRates.normalize(self.exchange_rates_B)
        )

    def suitably_cointegrated(self):
        return self.p_value() <= config.acceptable_coint_threshold

    def p_value(self):
        return self.analysis[1]

    def generate_cointegrated_pair(self):
        return CointegratedPair(
            pair=self.pair,
            cointegration_analysis=self.analysis,
            spreads=self.spreads(),
            exchange_rates=self.exchange_rates
        )

    def get_asset_exchange_rates(self):
        self.exchange_rates_A, self.exchange_rates_B = ExchangeRates.get_exchange_rates_from_candles(
            self.candles,
            self.pair,
        )

    def asset_lengths_equal(self):
        return len(self.exchange_rates_A) == len(self.exchange_rates_B)

    def spreads(self):
        returns_A = pd.DataFrame(self.exchange_rates_A).pct_change()
        returns_B = pd.DataFrame(self.exchange_rates_B).pct_change()

        return returns_A - returns_B
