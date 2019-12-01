from position_rules import PositionRules
from currency_convertor import CurrencyConvertor

class OrderRemover:
    def __init__(
        self,
        wallet,
        exchange_rates,
        cointegrated_pairs
    ):
        self.wallet = wallet
        self.exchange_rates = exchange_rates
        self.cointegrated_pairs = cointegrated_pairs

    def reverse_positions(self, order):
        short_exchange_rate = self.exchange_rates[order.short_position.asset]
        short_volume = order.short_position.volume
        long_exchange_rate = self.exchange_rates[order.long_position.asset]
        long_volume = order.long_position.volume

        self.wallet.buy(
            order.short_position.asset[:3],
            short_exchange_rate,
            short_volume
        )

        current_short_value_btc = CurrencyConvertor.asset_vol_to_btc_vol(
            short_exchange_rate,
            short_volume
        )
        short_difference = order.initial_short_value_btc() - current_short_value_btc
        self.wallet.rolling_profit += short_difference

        self.wallet.sell(
            order.long_position.asset[:3],
            long_exchange_rate,
            long_volume
        )

        current_long_value_btc = CurrencyConvertor.asset_vol_to_btc_vol(
            long_exchange_rate,
            long_volume
        )
        long_difference = order.initial_long_value_btc() - current_long_value_btc
        self.wallet.rolling_profit -= long_difference

    def for_non_cointegration(self, current_orders):
        co = []
        for order in current_orders:
            if not order.pair in [cp.pair for cp in self.cointegrated_pairs]:
                self.reverse_positions(order)
            else:
                co.append(order)
        return co

    def for_profit_loss(self, z_out, current_orders):
        co = []
        for order in current_orders:
            cp = [cp for cp in self.cointegrated_pairs if cp.pair == order.pair][0]
            if PositionRules.close_for_profit_loss(cp, order, z_out):
                self.reverse_positions(order)
            else:
                co.append(order)
        return co
