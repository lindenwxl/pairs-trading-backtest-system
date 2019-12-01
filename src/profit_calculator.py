import config
from currency_convertor import CurrencyConvertor

class ProfitCalculator:
    @classmethod
    def wallet_value_btc(self, wallet, exchange_rates):
        total = wallet.volumes['BTC']
        for asset, volume in wallet.volumes.items():
            if not asset == 'BTC':
                total += CurrencyConvertor.asset_vol_to_btc_vol(
                    volume,
                    exchange_rates[asset+'BTC']
                )
        return total

    @classmethod
    def change_in_btc_volume(self, wallet, exchange_rates):
        return wallet.current_btc_volume() - wallet.starting_btc_volume

    @classmethod
    def change_in_btc_volume_pct(self, wallet, exchange_rates):
        return (self.change_in_btc_volume(wallet, exchange_rates)/wallet.starting_btc_volume) * 100.0

    @classmethod
    def avg_btc_change_as_pct_of_order_value(self, wallet, exchange_rates, order_count):
        if order_count != 0:
            avg_change_per_order = self.change_in_btc_volume_pct(
                wallet,
                exchange_rates
            )/order_count
            return (avg_change_per_order/config.btc_order_volume)*100.0
        else:
            return 0.0
