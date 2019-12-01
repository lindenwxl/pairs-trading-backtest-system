from position import Position
from order import Order
import logger
import config
import helpers
from currency_convertor import CurrencyConvertor

class OrderBuilder:
    def __init__(self, cp, wallet):
        self.cp = cp
        self.wallet = wallet

    def place(self, short, long, current_orders):
        print 'placing order'
        order = Order(
            self.cp.pair,
            self.cp.current_spread,
            long,
            short
        )
        current_orders.append(order)
        return order

    def short_B_long_A(self):
        short = self.short_position(
            self.cp.asset_B(),
            self.cp.price_B()
        )
        long = self.long_position(
            self.cp.asset_A(),
            self.cp.price_A()
        )
        return [short, long]

    def short_A_long_B(self):
        short = self.short_position(
            self.cp.asset_A(),
            self.cp.price_A()
        )
        long = self.long_position(
            self.cp.asset_B(),
            self.cp.price_B()
        )
        return [short, long]

    def short_position(self, asset, exchange_rate):
        return Position(
            asset=asset,
            volume=self.wallet.sell(
                asset[:3],
                exchange_rate,
                CurrencyConvertor.btc_vol_to_asset_vol(config.btc_order_volume, exchange_rate)
            ),
            exchange_rate=exchange_rate
        )

    def long_position(self, asset, exchange_rate):
        return Position(
            asset=asset,
            volume=self.wallet.buy(
                asset[:3],
                exchange_rate,
                CurrencyConvertor.btc_vol_to_asset_vol(config.btc_order_volume, exchange_rate)
            ),
            exchange_rate=exchange_rate
        )
