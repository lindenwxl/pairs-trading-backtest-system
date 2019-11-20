from position_rules import PositionRules

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
        self.wallet.buy(
            order.short_position.asset[:3],
            self.exchange_rates[order.short_position.asset],
            order.short_position.volume
        )
        self.wallet.sell(
            order.long_position.asset[:3],
            self.exchange_rates[order.long_position.asset],
            order.long_position.volume
        )

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
