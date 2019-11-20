import numpy

class CointegratedPair:
    def __init__(
        self,
        pair,
        cointegration_analysis,
        spreads,
        exchange_rates
    ):
        self.pair = pair
        self.cointegration_analysis = cointegration_analysis
        self.spreads = spreads
        self.exchange_rates = exchange_rates

    def asset_A(self):
        return self.pair[0]

    def price_A(self):
        return self.exchange_rates[self.asset_A()]

    def asset_B(self):
        return self.pair[1]

    def price_B(self):
        return self.exchange_rates[self.asset_B()]

    def current_spread(self):
        return self.spreads.iloc[-2]

    def mean_spread(self):
        return self.spreads.mean().iloc[0]

    def p_value(self):
        return self.cointegration_analysis[1]

    def t_score(self):
        return self.cointegration_analysis[0]

    def z_score(self):
        return (self.current_spread() - self.mean_spread()) / self.spreads.std().iloc[0]
